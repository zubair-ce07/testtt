"""techlancers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework.authtoken import views as drf_views
from api.views.user_create_view import UserCreate
from api.views.current_user_info_view import CurrentUserInfoView
from api.views.freelancer_list_view import ListFreelancerView

app_name = 'api'
urlpatterns = [
    url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    url(r'^register_user$', UserCreate.as_view(), name='register_user'),
    url(r'^current_user$', CurrentUserInfoView.as_view(), name='current_user'),
    url(r'^freelancers$', ListFreelancerView.as_view(), name='list_freelancers')
]
