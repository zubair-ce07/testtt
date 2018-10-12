"""
this module contains all the urls of this app
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'my_user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.UserLoginFormView.as_view(), name='login'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', login_required(views.UserEditFormView.as_view(), login_url='/login'),
         name='edit'),
    path('change-password/', login_required(views.UserEditPassword.as_view(), login_url='/login'),
         name='change_password'),

    # following are urls for using REST Framework
    path('rest/', views.RestIndexView.as_view(), name='rest_index'),
    path('rest/login/', views.RestUserLoginFormView.as_view(), name='rest_login'),
    path('rest/register/', views.RestUserFormView.as_view(), name='rest_register'),
    path('rest/logout/', views.rest_logout_view, name='rest_logout'),
    path('rest/edit-profile/',
         login_required(views.RestUserEditFormView.as_view(), login_url='/rest/login'),
         name='rest_edit'),
    path('rest/change-password/',
         login_required(views.RestUserEditPassword.as_view(), login_url='/rest/login'),
         name='rest_change_password'),
]
