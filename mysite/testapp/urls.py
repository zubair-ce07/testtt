from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views




urlpatterns = [
    url(r'^user$', views.UserListCreate.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^user/friends$', views.FriendList.as_view()),
    url(r'^user/friend/(?P<friend_id>[0-9]+)$', views.FriendCreate.as_view()),
    url(r'^post', views.PostListCreate.as_view()),
    url(r'^comment/(?P<post_id>[0-9]+)/$', views.CommentListCreate.as_view()),
    url(r'^like/(?P<post_id>[0-9]+)/$', views.LikeListCreate.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)