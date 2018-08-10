from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path(r'signup/', views.SignUpView.as_view(), name='signup'),
    path(r'signup/signup_successful/', views.login_view, name='login')
]