from django.conf.urls import url
from backend.users.views.interests import UserInterestAPIView
from backend.users.views.profile import UserProfileAPIView
from backend.users.views.create import UserCreateAPIView
from rest_framework.authtoken import views

app_name = 'users'
urlpatterns = [
    url(r'interests/?', UserInterestAPIView.as_view(), name='interests'),
    url(r'profile/?', UserProfileAPIView.as_view(), name='profile'),
    url(r'create/?', UserCreateAPIView.as_view(), name='create'),
    url(r'authenticate/?', views.obtain_auth_token, name='authenticate'),
]
