

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


def all_designer_view(request : HttpRequest):

	return render(request, 'designer/all_designer_view.html')