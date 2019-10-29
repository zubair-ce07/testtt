"""
Users urls module.

This module has urls for users app.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from users import views

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', TemplateView.as_view(template_name='users/profile.html'), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('users_info/', views.UserListView.as_view(), name='users'),
    path('users_info/<int:pk>/view_info', views.view_info, name='view_info')

]
