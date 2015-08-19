from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from eproperty.decorators import is_logged_in
from web.users.views.dashboard import DashboardView
from web.users.views.activate_users import ActivateUsersView
from web.users.views.change_password import ChangePasswordView
from web.users.views.deactivate_users import DeactivateUsersView
from web.users.views.index import IndexView
from web.users.views.login import LogInView
from web.users.views.logout import LogoutView
from web.users.views.profile import ProfileView
from web.users.views.sign_up import SignUpView


urlpatterns = [
    url(r'^$', is_logged_in(IndexView.as_view()), name='index'),
    url(r'^login/$', is_logged_in(LogInView.as_view()), name='login'),
    url(r'^sign-up/$', is_logged_in(SignUpView.as_view()), name='sign_up'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^account/password/reset/$', login_required(ChangePasswordView.as_view()), name='change_password'),
    url(r'^account/logout/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^account/profile/$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^inactivate-users/$', login_required(DeactivateUsersView.as_view()), name='deactivate_users'),
    url(r'^activate-users/$', login_required(ActivateUsersView.as_view()), name='activate_users'),
]