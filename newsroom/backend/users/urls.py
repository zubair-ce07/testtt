from django.conf.urls import url
from backend.users.views.interests import UserInterestAPIView
from backend.users.views.profile import UserProfileAPIView


app_name = 'users'
urlpatterns = [
    url(r'interests/?', UserInterestAPIView.as_view()),
    url(r'profile/?', UserProfileAPIView.as_view()),
]
