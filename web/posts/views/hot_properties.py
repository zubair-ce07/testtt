from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post
from web.posts.serializers.post_serializer import PostSerializer


class HotPropertiesViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        posts = Post.objects.filter(is_expired=False)
        return sorted(posts, key=lambda post: -post.number_of_views);