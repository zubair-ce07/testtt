from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url

from users.views import (
    user_signupview,
    user_signinview,
    user_signoutview,
    user_change_passwordview,
    user_edit_profileview,
    error_view,
)

urlpatterns = [
    path('', user_signupview, name='signup'),
    path('signup/', user_signupview, name='signup'),
    path('signin/', user_signinview, name='signin'),
    path('signout/', user_signoutview, name='signout'),
    path('change_password/', user_change_passwordview, name='change_password'),
    path('edit_profile/', user_edit_profileview, name='edit_profile'),
    path('home/', TemplateView.as_view(template_name='users/home.html'), name='signin'),
    url(r'^.*', error_view),
]
