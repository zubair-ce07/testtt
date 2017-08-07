from django.conf.urls import url
from comment.views import APICommentList

urlpatterns = [
    url(r'^comment/$', APICommentList.as_view(), name='comment'),
]
