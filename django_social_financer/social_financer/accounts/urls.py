from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path(r'accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home_view, name='home'),
    path('my_consumers/', views.donors_pairs, name='my_consumers'),
]