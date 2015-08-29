from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from web.users.views.profile import ProfileViewSet
from web.users.views.sign_up import SignUpViewSet
from web.constants import *

urlpatterns = [
    url(r'^sign-up/$', SignUpViewSet.as_view(METHOD_POST_CREATE), name='sign_up'),
    url(r'^profile/(?P<pk>\d+)$', ProfileViewSet.as_view(METHOD_GET_RETRIEVE), name='profile'),
]