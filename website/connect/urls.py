from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'connect/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'connect/login.html' }, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/$', views.profile, name='profile'),
    url('^signup/$', views.create_user, name='create_user'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
]