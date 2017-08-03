from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from backend.users.views.interests import UserInterestViewSet


# router = DefaultRouter()
# router.register(r'users', UserInterestViewSet)
# print(router.urls)

app_name = 'users'
urlpatterns = [
    url(r'interests/?', UserInterestViewSet.as_view()),
]
