from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^logout/$', views.signout, name="signout"),
    url(r'^change_role/$', views.change_role, name="change_role"),
]
