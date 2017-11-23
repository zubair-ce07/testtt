from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^post/id/(?P<pk>[0-9]+)/$', views.view_post.as_view(), name='post'),

    url(r'^post/allPosts/$', views.list_posts.as_view(), name='all_posts'),
    #
    # url(r'^(?P<post_id>[0-9]+)/upvote/$', views.Like_Post.upvote, name='upvote'),
    #
    # url(r'^(?P<post_id>[0-9]+)/downvote/$', views.Like_Post.upvote, name='downvote'),
    #
    # url(r'^post/category/(?P<category>\w+)/$', views.Post.posts_by_category, name='by_category'),

    # url(r'^/post/(?P<user>\w+)/$', views.vote, name='vote'),
]