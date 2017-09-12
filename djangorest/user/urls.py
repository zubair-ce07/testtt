from django.conf.urls import url
from user.views import Login, APISignUp, APILogout


urlpatterns = [
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^signup$', APISignUp.as_view(), name='signup'),
    url(r'^logout$', APILogout.as_view(), name='logout'),
]
