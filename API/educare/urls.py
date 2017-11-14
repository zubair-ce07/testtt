from .views import (
    TutorSignUpView, UserLoginView,
    UserProfileChangeAPIView, ResetPasswordView,
    UserProfileView, TutorListView,
    StudentSignUpView, StudentListView,
    CreateFeedbackView, ListFeedbackView,
    CreateInviteView, ListInviteView,
    AcceptInviteView, DeleteInviteView
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
    url(r'^viewprofile/(?P<username>[\w-]+)/givefeedback/$', CreateFeedbackView.as_view(), name='GiveFeedback'),
    url(r'^viewprofile/(?P<username>[\w-]+)/viewallfeedbacks/$', ListFeedbackView.as_view(), name='ShowFeedbacks'),
    url(r'^viewprofile/(?P<username>[\w-]+)/sendinvite/$', CreateInviteView.as_view(), name='SendInvite'),
    url(r'^viewprofile/(?P<username>[\w-]+)/viewallinvites/$', ListInviteView.as_view(), name='ShowInvite'),
    url(r'^viewprofile/(?P<username>[\w-]+)/viewallinvites/acceptinvite/(?P<pk>[\d-]+)/$', AcceptInviteView.as_view(),
        name='ShowInvite'),
    url(r'^viewprofile/(?P<username>[\w-]+)/deleteinvite/(?P<pk>[\d-]+)/$', DeleteInviteView.as_view(),
        name='DeleteInvite'),
]
