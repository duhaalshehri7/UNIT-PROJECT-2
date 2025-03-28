

from django.shortcuts import render, redirect



from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from users.models import DesignerPost,Bookmark
from .models import Comment

def all_designer_view(request : HttpRequest):
	posts = DesignerPost.objects.all()
	return render(request, 'designer/all_designer_view.html', {'posts': posts})








def post_to_user_view(request, post_id):
    try:
        profile = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        return redirect('main:main_page_view')


    is_bookmarked = False
    if request.user.is_authenticated and not request.user.is_designer:
        is_bookmarked = Bookmark.objects.filter(user=request.user, designer_post=profile).exists()



    if request.method == 'POST':
        if request.user.is_authenticated and not request.user.is_designer:
            rating = request.POST.get('rating')
            comment_text = request.POST.get('comment')

            if rating and comment_text:
                Comment.objects.create(
                    designer_post=profile,
                    user=request.user,
                    rating=int(rating),
                    comment=comment_text
                )
                return redirect('designer:post_to_user_view', post_id=post_id)

    comments = profile.comments.all().order_by('-created_at')

    return render(request, 'designer/view_post_to_user.html', {'profile': profile,'comments': comments,'is_bookmarked': is_bookmarked,})
