from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='registration/base.html'), name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^home$', views.home, name='home'),
]