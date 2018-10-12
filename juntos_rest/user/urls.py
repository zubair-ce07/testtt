from django.conf.urls import url

from .views import ProfileView, RegisterApiView, UserListApiView

urlpatterns = [
    url('profile/', ProfileView.as_view()),
    url('profiles/', UserListApiView.as_view()),
    url('register/', RegisterApiView.as_view()),
]
