from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from eproperty.decorators import is_logged_in
from web.users.views.account import AccountView
from web.users.views.activate_users import ActivateUsersView
from web.users.views.change_password import ChangePasswordView
from web.users.views.deactivate_users import DeactivateUsersView
from web.users.views.edit_profile import EditProfileView
from web.users.views.index import IndexView
from web.users.views.login import LogInView
from web.users.views.logout import LogoutView
from web.users.views.profile import ProfileView
from web.users.views.sign_up import SignUpView


urlpatterns = [
    url(r'^$', is_logged_in(IndexView.as_view()), name='index'),
    url(r'^login/$', is_logged_in(LogInView.as_view()), name='login'),
    url(r'^sign-up/$', is_logged_in(SignUpView.as_view()), name='sign_up'),
    url(r'^account/$', login_required(AccountView.as_view()), name='account'),
    url(r'^account/password/reset/$', login_required(ChangePasswordView.as_view()), name='change_password'),
    url(r'^account/logout/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^account/profile/$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^account/profile/edit/$', login_required(EditProfileView.as_view()), name='edit_profile'),
    url(r'^inactivate-users/$', login_required(DeactivateUsersView.as_view()), name='deactivate_users'),
    url(r'^activate-users/$', login_required(ActivateUsersView.as_view()), name='activate_users'),
]