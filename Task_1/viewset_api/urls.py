from django.conf.urls import url
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from viewset_api import views

app_name = 'viewset'

urlpatterns = format_suffix_patterns([
    url('^$', views.api_root),
    url(r'list/$', views.UserViewSet.as_view({'get': 'list'}), name='list'),
    url(r'(?P<pk>[0-9]+)/details/$',
        views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'}),
        name='details'),
    url(r'login/$', views.Login.as_view({'get': 'retrieve', 'post': 'submit'}), name='login'),
    url(r'logout/$', views.Logout.as_view({'get': 'get'}), name='logout'),
    url(r'signup/$', views.Signup.as_view({'get': 'retrieve'}), name='signup'),

])
