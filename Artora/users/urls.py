
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signas/', views.sign_up_as_view, name='sign_up_as_view'),
    path('signup/client', views.client_signup_view, name='client_signup_view'),
    path('signup/designer', views.designer_signup_view, name='designer_signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<str:user_name>/', views.user_profile_view, name='user_profile_view'),

]