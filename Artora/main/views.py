from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from users.models import DesignerPost, DesignerProfile

from django.db.models import Avg

# Create your views here.






def main_page_view(request):
    post1 = None
    if request.user.is_authenticated and request.user.is_designer:
        try:
            designer_profile = DesignerProfile.objects.get(user=request.user)
            post1 = DesignerPost.objects.get(designer=designer_profile)
        except (DesignerProfile.DoesNotExist, DesignerPost.DoesNotExist):
            post1 = None

    if request.user.is_authenticated:
      print(f"User {request.user.username} is logged in.")
    else:
      	print("User is NOT logged in.")



    grouped_designers = {}

    for value, label in DesignerProfile.Specialty.choices:
        designers = DesignerPost.objects.filter(designer__specialty=value)
        grouped_designers[label] = designers


    return render(request, 'main/main_page.html', {'post1': post1,"grouped_designers": grouped_designers,})





def about_page_view(request):
    return render(request, 'main/about_us.html')