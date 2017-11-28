from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^post/id/(?P<pk>[0-9]+)/$', views.view_post.as_view(), name='post'),

    url(r'^post/allPosts/$', views.list_posts.as_view(), name='all_posts'),
]
