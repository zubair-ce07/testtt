from django.contrib import admin
from django.urls import path

from account import views
from account.views import login_view

urlpatterns = [
    path(
        'account/login/',
        login_view,
        name="login"),
    path(
        'account/login/successful_login',
        views.successful_login,
        name="successful_login"),
    path(
        'account/login/edit_profile',
        views.editprofile,
        name="edit_profile"),
    path(
        'account/change_password',
        views.changepassword,
        name="change_password"),
    path(
        'admin/',
        admin.site.urls),
]
