from django.conf.urls import url
from comment.views import APICommentList, APICommentDetail

urlpatterns = [
    url(r'^comment/$', APICommentList.as_view(), name='comment'),
    url(r'^comment/(?P<pk>[0-9]+)/$', APICommentDetail.as_view(), name='detail'),
]
