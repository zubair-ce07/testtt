from django.conf.urls import url
from web.posts.views.all_posts import AllPostsViewSet
from web.posts.views.my_posts import MyPostsViewSet
from web.posts.views.new_post import NewPostViewSet
from web.posts.views.post_details import PostDetailsViewSet
from web.posts.views.process_request import ProcessRequestViewSet
from web.posts.views.my_requests import MyRequestsViewSet
from web.posts.views.requests_on_post import RequestsOnPostViewSet
from web.posts.views.new_request import NewRequestViewSet
from web.constants import *


urlpatterns = [
    url(r'^posts/my-posts$', MyPostsViewSet.as_view(METHOD_GET_LIST), name='my_posts'),
    url(r'^my-requests/$', MyRequestsViewSet.as_view(METHOD_GET_LIST), name='my_requests'),
    url(r'^posts/all$', AllPostsViewSet.as_view(METHOD_GET_LIST), name='all_posts'),
    url(r'^posts/(?P<pk>\d+)$', PostDetailsViewSet.as_view(METHOD_GET_RETRIEVE), name='post_details'),
    url(r'^posts/new$', NewPostViewSet.as_view(METHOD_POST_CREATE), name='new_post'),
    url(r'^posts/(?P<post_id>\d+)/request/new$', NewRequestViewSet.as_view(METHOD_POST_CREATE), name='new_request'),
    url(r'^posts/(?P<post_id>\d+)/requests$', RequestsOnPostViewSet.as_view(METHOD_GET_LIST), name='requests_on_posts'),
    url(r'^posts/(?P<post_id>\d+)/process-request/(?P<pk>\d+)$',
        ProcessRequestViewSet.as_view(merge(METHOD_PUT_UPDATE, METHOD_GET_RETRIEVE)),
        name='process_request'),
]