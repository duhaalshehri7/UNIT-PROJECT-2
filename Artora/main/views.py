from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def main_page_view(request : HttpRequest):
	if request.user.is_authenticated:
		print(f"User {request.user.username} is logged in.")
	else:
		print("User is NOT logged in.")

	return render(request, 'main/main_page.html')