from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from viewset_api import views

app_name = 'viewset'
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
# urlpatterns = router.urls
urlpatterns = format_suffix_patterns([
    url('^', include(router.urls)),
    url(r'list/$', views.UserViewSet.as_view({'get': 'list'}), name='list'),
    url(r'(?P<pk>[0-9]+)/details/$',
        views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'}),
        name='details'),
    url(r'login/$', views.Login.as_view({'get': 'get', 'post': 'post'}), name='login'),
    url(r'logout/$', views.Logout.as_view({'get': 'get'}), name='logout'),
    url(r'signup/$', views.Signup.as_view({'get': 'get', 'post': 'post'}), name='signup'),

])
