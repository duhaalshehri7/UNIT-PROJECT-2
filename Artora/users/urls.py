
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signas/', views.sign_up_as_view, name='sign_up_as_view'),
    path('signup/client', views.client_signup_view, name='client_signup_view'),
    path('signup/designer', views.designer_signup_view, name='designer_signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),



    path('post/create/', views.create_post_view, name='create_post_view'),
    path('post/edit/<post_id>/', views.edit_post_view, name='edit_post_view'),
    path('post/delete/<post_id>/', views.delete_post_view, name='delete_post_view'),
    path('post/view/<post_id>/', views.view_post_view, name='view_post_view'),
    path('bookmark/<post_id>/', views.add_bookmark_view, name='add_bookmark_view'),

    path('profile/<user_id>/', views.user_profile_view, name="user_profile_view"),
    path('profile/<int:user_id>/edit/', views.edit_user_profile_view, name='edit_user_profile_view'),

]