from django.conf.urls import url
from web.constants import METHOD_GET_LIST, METHOD_GET_RETRIEVE, METHOD_POST_CREATE, METHOD_PUT_UPDATE, merge
from web.posts.views.all_posts import AllPostsViewSet
from web.posts.views.customized_search import CustomizedSearchViewSet
from web.posts.views.hot_properties import HotPropertiesViewSet
from web.posts.views.my_posts import MyPostsViewSet
from web.posts.views.new_post import NewPostViewSet
from web.posts.views.post_details import PostDetailsViewSet
from web.posts.views.process_request import ProcessRequestViewSet
from web.posts.views.my_requests import MyRequestsViewSet
from web.posts.views.requests_on_post import RequestsOnPostViewSet
from web.posts.views.new_request import NewRequestViewSet


urlpatterns = [
    url(r'^posts/my-posts/$', MyPostsViewSet.as_view(METHOD_GET_LIST), name='my_posts'),
    url(r'^my-requests/$', MyRequestsViewSet.as_view(METHOD_GET_LIST), name='my_requests'),
    url(r'^posts/all/$', AllPostsViewSet.as_view(METHOD_GET_LIST), name='all_posts'),
    url(r'^posts/hot/$', HotPropertiesViewSet.as_view(METHOD_GET_LIST), name='hot_posts'),
    url(r'^posts/search/$', CustomizedSearchViewSet.as_view(METHOD_GET_LIST), name='search_posts'),
    url(r'^posts/(?P<pk>\d+)/$', PostDetailsViewSet.as_view(METHOD_GET_RETRIEVE), name='post_details'),
    url(r'^posts/new/$', NewPostViewSet.as_view(METHOD_POST_CREATE), name='new_post'),
    url(r'^posts/(?P<post_id>\d+)/request/new/$', NewRequestViewSet.as_view(METHOD_POST_CREATE), name='new_request'),
    url(r'^posts/(?P<post_id>\d+)/requests/$', RequestsOnPostViewSet.as_view(METHOD_GET_LIST), name='requests_on_posts'),
    url(r'^posts/(?P<post_id>\d+)/process-request/(?P<pk>\d+)/$',
        ProcessRequestViewSet.as_view(merge(METHOD_PUT_UPDATE, METHOD_GET_RETRIEVE)),
        name='process_request'),
]