from django.conf.urls import url
from user.views import Login, Logout, SignUp, Update

app_name = 'wblog_user'

urlpatterns = [
    url(r'^(?P<pk>[a-z_]+)/$', Update.as_view(), name='update'),
    url(r'^create$', SignUp.as_view(), name='signup'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^$', Login.as_view(), name='login'),
]
