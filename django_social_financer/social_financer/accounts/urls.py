from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'
urlpatterns = [
    path(r'signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path(r'accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path(r'', views.home_view, name='home'),
]