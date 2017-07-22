from django.conf.urls import url, include
from .views import Login, SignupView, profile_view, Logout


app_name = 'wblog'

urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^profile$', profile_view, name='profile'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^$', Login.as_view(), name='login'),
]
