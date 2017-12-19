from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^post/id/(?P<pk>[0-9]+)/$', views.ViewPost.as_view(), name='post'),

    url(r'^post/listposts/$', views.list_posts.as_view(), name='all_posts'),
]
