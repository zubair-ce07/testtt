from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from eproperty.decorators import is_logged_in
from web.users.views.account import AccountView
from web.users.views.login import LogInView
from web.users.views.sign_up import SignUpView


urlpatterns = [
    url(r'^$', is_logged_in(LogInView.as_view()), name='index'),
    url(r'^sign-up/$', is_logged_in(SignUpView.as_view()), name='sign_up'),
    url(r'^account/$', login_required(AccountView.as_view()), name='account'),
]