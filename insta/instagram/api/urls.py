from django.conf.urls import url
from instagram.api.views import *


urlpatterns = [
    url(r'^users/$', UserListAPIView.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailAPIView.as_view(), name='user-detail'),
    url(r'^posts/$', PostListAPIView.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)/$', PostDetailAPIView.as_view(), name='post-detail'),
    url(r'^likes/$', LikeListAPIView.as_view(), name='like-list'),
    url(r'^likes/(?P<pk>[0-9]+)/$', LikeDetailAPIView.as_view(), name='like-detail'),
    url(r'^comments/$', CommentListAPIView.as_view(), name='comment-list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', CommentDetailAPIView.as_view(), name='comment-detail'),
    url(r'^signup/$', UserSignupAPIView.as_view(), name='user-signup'),
    url(r'^signup/available/$', UsernameEmailAvailableAPIView.as_view(), name='user-signup2'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='user-login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='user-logout'),
    url(r'^newsfeed/$', NewsfeedListAPIView.as_view(), name='user-newsfeed'),
]