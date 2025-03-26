
from django.shortcuts import render, redirect
from .forms import ClientSignUpForm, DesignerSignUpForm,DesignerPostForm
from django.http import HttpRequest, HttpResponse

from .models import CustomUser,DesignerPost, DesignerPostImage, DesignerProfile

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





def user_profile_view(request: HttpRequest, user_name: str):
    try:
        user = CustomUser.objects.get(username=user_name)

        designer_profile = None
        if user.is_designer:
            try:
                designer_profile = DesignerProfile.objects.get(user=user)
            except DesignerProfile.DoesNotExist:
                designer_profile = None
    except CustomUser.DoesNotExist:
        return print("User not found")

    return render(request, 'profiles/profile.html', {"user": user,"designer_profile": designer_profile})


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
        pass  # No post found, post is set to None

    if request.method == 'POST':
        form = DesignerPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.designer = designer_profile
            post.save()

            work_samples = request.FILES.getlist('work_samples')
            for image in work_samples:
                DesignerPostImage.objects.create(designer_post=post, image=image)

            messages.success(request, "Your post has been created!")
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
            messages.success(request, "Your post has been updated!")
            return redirect('users:edit_post_view', post_id=post.id)
    else:
        form = DesignerPostForm(instance=post)

    return render(request, 'designer/edit_post.html', {'form': form, 'post': post})



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
        messages.success(request, "Your post has been deleted!")
        return redirect('users:create_post_view')


    return redirect('users:edit_post_view', post_id=post.id)




def view_post_view(request, post_id):
    try:
        post1 = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        post1 = None

    return render(request, 'designer/view_post.html', {'post1': post1})
