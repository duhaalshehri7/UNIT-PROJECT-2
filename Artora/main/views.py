from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.


# def main_page_view(request : HttpRequest):
# 	if request.user.is_authenticated:
# 		print(f"User {request.user.username} is logged in.")
# 	else:
# 		print("User is NOT logged in.")
#
# 	return render(request, 'main/main_page.html')
#
#


from users.models import DesignerProfile, DesignerPost

def main_page_view(request):
    post1 = None
    if request.user.is_authenticated and request.user.is_designer:
        try:
            designer_profile = DesignerProfile.objects.get(user=request.user)
            post1 = DesignerPost.objects.get(designer=designer_profile)
        except (DesignerProfile.DoesNotExist, DesignerPost.DoesNotExist):
            post1 = None

    return render(request, 'main/main_page.html', {'post1': post1})
