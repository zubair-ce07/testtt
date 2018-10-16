from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from web.account.views import (
    EditProfileView, UserDashboardView, UserStatsView,
    UserType, CustomerRegisterView, ManagerRegisterView
)

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='account/login.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user='account:dashboard'
    ), name="login"),
    path('register/customer/', CustomerRegisterView.as_view(), name="customer_register"),
    path('register/manager/', ManagerRegisterView.as_view(), name="manager_register"),
    path('user-type/', UserType.as_view(), name="usertype"),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('stats/', UserStatsView.as_view(), name='stats'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name="edit"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
