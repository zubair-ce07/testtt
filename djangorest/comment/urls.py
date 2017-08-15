from django.conf.urls import url
from comment.views import CommentCreate, CommentUpdateDelete

urlpatterns = [
    url(r'^$', CommentCreate.as_view(), name='comment'),
    url(r'^(?P<pk>[0-9]+)/$', CommentUpdateDelete.as_view(), name='comment_update_delete'),
]
