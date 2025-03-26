

from django.shortcuts import render, redirect



from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from users.models import DesignerPost


def all_designer_view(request : HttpRequest):
	posts = DesignerPost.objects.all()
	return render(request, 'designer/all_designer_view.html', {'posts': posts})





def post_to_user_view(request, post_id):
    try:
        profile = DesignerPost.objects.get(id=post_id)
    except DesignerPost.DoesNotExist:
        return redirect('main:main_page_view')

    return render(request, 'designer/view_post_to_user.html', {'profile': profile})
