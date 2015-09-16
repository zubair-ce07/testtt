from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post
from web.posts.serializers.post_serializer import PostSerializer


class AllPostsViewSet(mixins.ListModelMixin, GenericViewSet):

    queryset = Post.objects.filter(is_expired=False).order_by('-id')
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)