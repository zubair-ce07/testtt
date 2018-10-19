from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Blog, Tag, Comment
from .serializers import BlogSerializer, TagSerializer, CommentSerializer
from .permissions import IsWriterOrReadOnly


class TagMixin:
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TagList(TagMixin, ListCreateAPIView):
    pass


class TagDetail(TagMixin, RetrieveUpdateDestroyAPIView):
    pass


class BlogMixin:
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsWriterOrReadOnly,)


class BlogList(BlogMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class BlogDetail(BlogMixin, RetrieveUpdateDestroyAPIView):
    pass


class CommentMixin:
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsWriterOrReadOnly,)


class CommentList(CommentMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all()

        try:
            blog_id = int(self.request.query_params.get('blog_id'))

            if blog_id:
                queryset = queryset.filter(
                    object_id=blog_id, content_type__model='blog')
        except ValueError:
            pass

        return queryset


class CommentDetail(CommentMixin, RetrieveUpdateDestroyAPIView):
    pass
