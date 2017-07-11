from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
# app_name = 'instagram'

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'instagram/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^search/$', views.search, name='search'),
    url(r'^$', views.index, name='index'),

    # url(r'^search_form/$', views.search_form),
    # url(r'^search/$', views.search),
]