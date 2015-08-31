from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Request, Post
from web.posts.permissions import IsPostOfCurrentUser
from web.posts.serializers.process_request_serializer import ProcessRequestSerializer


class ProcessRequestViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericViewSet):

    serializer_class = ProcessRequestSerializer
    permission_classes = (permissions.IsAuthenticated, IsPostOfCurrentUser)

    def get_queryset(self):
        self.queryset = Request.objects.filter(post=Post.objects.get(pk=self.kwargs.get('post_id')))
        return self.queryset



