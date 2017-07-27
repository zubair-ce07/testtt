from .views import (
    TutorSignUpView, UserLoginView,
    UserProfileChangeAPIView, ResetPasswordView,
    UserProfileView, TutorListView,
    StudentSignUpView, StudentListView,
    )
from django.conf.urls import url
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^register/student/', StudentSignUpView.as_view(), name='StudentSignUp'),
    url(r'^register/tutor/', TutorSignUpView.as_view(), name='TutorSignUp'),
    url(r'^auth/token', views.obtain_auth_token),
    url(r'^login/', UserLoginView.as_view(), name='Login'),
    url(r'^tutorlist/', TutorListView.as_view(), name='TutorList'),
    url(r'^studentlist/', StudentListView.as_view(), name='StudentList'),
    url(r'^editprofile/(?P<username>[\w-]+)$', UserProfileChangeAPIView.as_view(), name='EditProfile'),
    url(r'^resetpassword/(?P<username>[\w-]+)$', ResetPasswordView.as_view(), name='PasswordReset'),
    url(r'^viewprofile/(?P<username>[\w-]+)$', UserProfileView.as_view(), name='ViewProfile'),
]
