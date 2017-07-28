from django.conf.urls import url
from user.views import APILogin, APISignUp


urlpatterns = [
    url(r'^login/$', APILogin.as_view(), name='login'),
    url(r'^signup/$', APISignUp.as_view(), name='signup'),
]
