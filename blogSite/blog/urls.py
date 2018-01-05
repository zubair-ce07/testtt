from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^post/id/(?P<pk>[0-9]+)/$', views.ViewPost.as_view(), name='post'),

    url(r'^post/listposts/$', views.ListPosts.as_view(), name='all_posts'),

    url(r'^post/createpost/$', views.CreatePost.as_view(), name='create_post'),
]
