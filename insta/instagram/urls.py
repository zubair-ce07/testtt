from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
# app_name = 'instagram'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^search/$', views.search, name='search'),
    # url(r'^profiles/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    # url(r'^profiles/(?P<pk>[0-9]+)/follow/$', views.follow_profile, name='follow'),
    # url(r'^profiles/(?P<pk>[0-9]+)/unfollow/$', views.unfollow_profile, name='unfollow'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),

    # url(r'^search_form/$', views.search_form),
    # url(r'^search/$', views.search),
]