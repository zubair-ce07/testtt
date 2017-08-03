from django.conf.urls import url

from generic_api import views

app_name = 'generic'

urlpatterns = [
    url('^$', views.api_root),
    url(r'list/$', views.UserList.as_view(), name='list'),
    url(r'(?P<pk>[0-9]+)/details/$', views.UserDetails.as_view(), name='details'),
    url(r'login/$', views.Login.as_view(), name='login'),
    url(r'signup/$', views.Signup.as_view(), name='signup'),
    url(r'logout/$', views.Logout.as_view(), name='logout'),
    url(r'edit/$', views.EditProfile.as_view(), name='edit'),
]
