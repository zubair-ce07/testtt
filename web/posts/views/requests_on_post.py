from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Request, Post
from web.posts.serializers.request_serializer import RequestSerializer


class RequestsOnPostViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(pk=post_id)
        if current_user == post.posted_by:
            queryset = Request.objects.filter(post=post).order_by('-id')
        else:
            queryset = Request.objects.filter(post=post, requested_by=current_user).order_by('-id')
        return queryset
