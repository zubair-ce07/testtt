from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Blog, Tag, Comment
from .serializers import BlogSerializer, TagSerializer, CommentSerializer
from .permissions import IsWriterOrReadOnly


class TagMixin(object):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TagList(TagMixin, ListCreateAPIView):
    pass


class TagDetail(TagMixin, RetrieveUpdateDestroyAPIView):
    pass


class BlogMixin(object):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsWriterOrReadOnly,)


class BlogList(BlogMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class BlogDetail(BlogMixin, RetrieveUpdateDestroyAPIView):
    pass


class CommentMixin(object):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsWriterOrReadOnly,)


class CommentList(CommentMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class CommentDetail(CommentMixin, RetrieveUpdateDestroyAPIView):
    pass
