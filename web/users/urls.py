from django.conf.urls import url
from web.constants import METHOD_POST_CREATE, METHOD_GET_LIST, METHOD_PUT_UPDATE
from web.users.views.activate_users import ActivateUsersView
from web.users.views.change_password import ChangePasswordViewSet
from web.users.views.deactivate_users import DeactivateUsersView
from web.users.views.profile import ProfileViewSet
from web.users.views.sign_up import SignUpViewSet
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', SignUpViewSet.as_view(METHOD_POST_CREATE), name='sign_up'),
    url(r'^account/profile/$', ProfileViewSet.as_view(METHOD_GET_LIST), name='profile'),
    url(r'^account/profile/edit$', ProfileViewSet.as_view(METHOD_PUT_UPDATE), name='edit_profile'),
    url(r'^account/password/change$', ChangePasswordViewSet.as_view(METHOD_POST_CREATE), name='change_password'),
    url(r'^deactivate-users/$', login_required(DeactivateUsersView.as_view()), name='deactivate_users'),
    url(r'^activate-users/$', login_required(ActivateUsersView.as_view()), name='activate_users'),
]


