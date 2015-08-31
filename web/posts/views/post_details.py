from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post, PostView
from web.posts.serializers.post_serializer import PostSerializer


class PostDetailsViewSet(mixins.RetrieveModelMixin, GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """ Setting Queryset and saving the current user's view on this particular post if its not already there. """
        try:
            post_id = self.kwargs.get('pk')
            post = Post.objects.get(pk=post_id)
            if not PostView.objects.filter(post_viewed=post, viewed_by=self.request.user).exists():
                PostView(viewed_by=self.request.user, post_viewed=post).save()
        except Post.DoesNotExist:
            pass
        return Post.objects.filter(is_expired=False)
