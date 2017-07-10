from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'instagram/login.html'}, name='login'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^$', views.index, name='index'),

    # url(r'^search_form/$', views.search_form),
    # url(r'^search/$', views.search),
]