from django.conf.urls import patterns, include, url
from myapp import views


urlpatterns = patterns('',
                       url(r'^$', views.login_view, name='login'),
                       url(r'^login', views.login_view, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/myapp/'})
                       )
