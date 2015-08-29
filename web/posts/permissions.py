from rest_framework.permissions import BasePermission
from web.posts.models import Post, Request


class IsPostOfCurrentUser(BasePermission):

    def has_permission(self, request, view):
        post = Post.objects.filter(pk=request.parser_context.get('kwargs').get('post_id'))
        if post.exists():
            is_permitted = post[0].posted_by == request.user
        else:
            is_permitted = False
        return is_permitted


class IsNotPostOfCurrentUser(BasePermission):

    def has_permission(self, request, view):
        post = Post.objects.filter(pk=request.parser_context.get('kwargs').get('post_id'))
        if post.exists():
            is_permitted = post[0].posted_by != request.user
        else:
            is_permitted = False
        return is_permitted