from django.conf.urls import url
from . import views
from ehub.views import EditProfile
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.viewprofile, name='viewprofile'),
    url(r'^profile/edit/$', EditProfile.as_view(), name='editprofile'),
    url(r'login/$', views.login, name="login"),
    url(r'logout/$', views.logout, name="logout"),
]
