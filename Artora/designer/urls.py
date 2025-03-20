from django.urls import path
from . import views

app_name = 'designer'

urlpatterns = [
    path('designer/all/', views.all_designer_view, name='all_designer_view'),

]