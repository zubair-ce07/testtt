from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.training_index),
    url(r'^trainee/(?P<trainee_id>[0-9]+)/$', views.trainee_details),
    url(r'^trainer/(?P<trainer_id>[0-9]+)/$', views.trainer_details),
    url(r'^assignment/(?P<assignment_id>[0-9]+)/$', views.assignment_details),
    url(r'^technology/(?P<technology_id>[0-9]+)/$', views.technology_details),
    url(r'^search/$', views.search),
    url(r'^login/$', views.login)
]
