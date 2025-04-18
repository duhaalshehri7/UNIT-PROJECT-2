
from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, DesignerSignUpForm,DesignerPostForm
from django.http import HttpRequest, HttpResponse

from .models import CustomUser,DesignerPost, DesignerPostImage, DesignerProfile, Bookmark

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages



def sign_up_as_view(request : HttpRequest):
	return render(request, 'users/sign_up_as.html')



def client_signup_view(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!', 'alert-success')
            return redirect('users:login_view')
    else:
        form = ClientSignUpForm()

    return render(request, 'users/signup_client.html', {'form': form})








def designer_signup_view(request):
    if request.method == 'POST':
        form = DesignerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_designer = True
            user.save()

            DesignerProfile.objects.create(
                user=user,
                specialty=request.POST.get('specialty'),
                experience=request.POST.get('experience'),
                location=request.POST.get('location'),
                experience_level=request.POST.get('experience_level'),
                pricing=request.POST.get('pricing'),
            )

            messages.success(request, 'Your account has been created!', 'alert-success')
            return redirect('main:main_page_view')
    else:
        form = DesignerSignUpForm()

    return render(request, 'users/signup_designer.html', {'form': form})







def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in!' ,'alert-success')
                return redirect('main:main_page_view')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:main_page_view')






def user_profile_view(request, user_id):
    try:
        profile_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "an error occurred.", "alert-danger")
        return redirect("main:main_page_view")

    designer_profile = None
    if profile_user.is_designer:
        designer_profile = DesignerProfile.objects.filter(user=profile_user).first()

    return render(request, 'profiles/profile.html', {
        'profile_user': profile_user,
        'designer_profile': designer_profile,
    })



def create_post_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login_view')

    user = request.user
    if not user.is_designer:
        return redirect('main:main_page_view')

    try:
        designer_profile = DesignerProfile.objects.get(user=user)
    except DesignerProfile.DoesNotExist:
        return redirect('main:main_page_view')

    post = None
    try:
        post = DesignerPost.objects.get(designer=designer_profile)
    except DesignerPost.DoesNotExist:
        pass

    if request.method == 'POST':
        form = DesignerPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.designer = designer_profile
            post.save()

            work_samples = request.FILES.getlist('work_samples')
            for image in work_samples:
                DesignerPostImage.objects.create(designer_post=post, image=image)

            messages.success(request, "Your post has been created!",'alert-success')
            return redirect('users:edit_post_view', post_id=post.id)
    else:
        form = DesignerPostForm()

    return render(request, 'designer/create_post.html', {'form': form, 'post': post})



def edit_post_view(request, post_id):
    if not request.user.is_authenticated:
        return redirect('users:login_view')

    user = request.user
    if not user.is_designer:
        return redirect('main:main_page_view')

    try:
        post = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        return redirect('main:main_page_view')

    if post.designer.user != user:
        return redirect('main:main_page_view')

    if request.method == 'POST':
        form = DesignerPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            work_samples = request.FILES.getlist('work_samples')
            for image in work_samples:
                DesignerPostImage.objects.create(designer_post=post, image=image)

            messages.success(request, "Your post has been updated!",'alert-success')
            return redirect('users:edit_post_view', post_id=post.id)
    else:
        form = DesignerPostForm(instance=post)

    work_samples = post.work_samples.all()
    return render(request, 'designer/edit_post.html', {'form': form, 'post': post, 'work_samples': work_samples})



def delete_post_view(request, post_id):
    if not request.user.is_authenticated:
        return redirect('users:login_view')

    user = request.user
    if not user.is_designer:
        return redirect('main:main_page_view')

    try:
        post = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        return redirect('main:main_page_view')

    if post.designer.user != user:
        return redirect('main:main_page_view')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Your post has been deleted!",'alert-success')
        return redirect('users:create_post_view')


    return redirect('users:edit_post_view', post_id=post.id)




def view_post_view(request, post_id):
    try:
        post1 = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        post1 = None

    return render(request, 'designer/view_post.html', {'post1': post1})



def add_bookmark_view(request, post_id):
    if not request.user.is_authenticated:
        messages.error(request, "Only registered users can add bookmarks", "alert-danger")
        return redirect("users:login_view")

    try:
        post = DesignerPost.objects.get(pk=post_id)

        bookmark = Bookmark.objects.filter(designer_post=post, user=request.user).first()
        if not bookmark:
            Bookmark.objects.create(user=request.user, designer_post=post)
            # messages.success(request, "Bookmark added", "alert-success")
        else:
            bookmark.delete()
            # messages.warning(request, "Bookmark removed", "alert-warning")

    except Exception as e:
        print("Bookmark error:", e)

    return redirect("designer:post_to_user_view", post_id=post_id)



def edit_user_profile_view(request, user_id):
    print("Logged in user ID:", request.user.id)
    print("URL user ID:", user_id)
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to edit your profile.", "alert-warning")
        return redirect("users:login_view")

    if request.user.id != user_id:
        messages.warning(request, "You cannot edit this profile", "alert-warning")
        return redirect("main:main_page_view")

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.", "alert-danger")
        return redirect("main:main_page_view")

    designer_profile = None
    if user.is_designer:
        designer_profile = DesignerProfile.objects.filter(user=user).first()

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        if user.is_designer:
            if designer_profile:
                designer_profile.specialty = request.POST.get("specialty")
                designer_profile.location = request.POST.get("location")
                designer_profile.experience = request.POST.get("experience")
                designer_profile.experience_level = request.POST.get("experience_level")
                designer_profile.pricing = request.POST.get("pricing")
                designer_profile.save()
        else:
            user.description = request.POST.get("description")

        user.save()
        messages.success(request, "Profile updated successfully!", "alert-success")
        return redirect("users:user_profile_view", user_id=user.id)

    return render(request, "profiles/update_profile.html", {
        "user": user,
        "designer_profile": designer_profile,
    })
