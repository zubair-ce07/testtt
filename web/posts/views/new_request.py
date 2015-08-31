from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Request, Post
from web.posts.serializers.request_serializer import RequestSerializer
from web.posts.permissions import IsNotPostOfCurrentUser


class NewRequestViewSet(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotPostOfCurrentUser)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        serializer.save(requested_by=self.request.user, post=post)

