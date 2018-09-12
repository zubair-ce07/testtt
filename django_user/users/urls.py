from django.urls import path
from django.conf.urls import url

from users.views import (
    user_signup_view,
    user_signin_view,
    user_signout_view,
    user_change_password_view,
    user_edit_profile_view,
    user_home_view,
)

urlpatterns = [
    path('', user_signup_view, name='signup'),
    path('signup/', user_signup_view, name='signup'),
    path('signin/', user_signin_view, name='signin'),
    path('signout/', user_signout_view, name='signout'),
    path('change_password/', user_change_password_view, name='change_password'),
    path('edit_profile/', user_edit_profile_view, name='edit_profile'),
    path('home/', user_home_view, name='home'),
]
