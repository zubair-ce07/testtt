from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post
from web.posts.serializers.post_serializer import PostSerializer


class MyPostsViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        self.queryset = Post.objects.filter(is_expired=False, posted_by=self.request.user)
        return self.queryset