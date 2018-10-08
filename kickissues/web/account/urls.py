from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from .views import (
    EditProfileView, RegisterView, UserDashboardView, UserStatsView,
    UserType
)

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='account/login.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user='account:dashboard'
    ), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    re_path(r'^register/(?P<type>\D+)/', RegisterView.as_view(), name="register"),
    path('user-type/', UserType.as_view(), name="usertype"),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('stats/', UserStatsView.as_view(), name='stats'),
    re_path(r'^edit/(?P<pk>\d+)/$', EditProfileView.as_view(), name="edit"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
