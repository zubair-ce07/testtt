from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Blog
from blog.serializers import BlogSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class APIBlogList(APIView):

    parser_classes = (JSONParser, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):
        return Response(BlogSerializer(Blog.objects.all(), many=True).data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request.data.update({'created_by': request.user.username,
                             'slug': request.data.get('title').lower().replace(' ', '_')})
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIBlogDetail(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, slug, format=None):
        blog = get_object_or_404(Blog, slug=slug)
        comments = CommentSerializer(Comment.objects.filter(comment_for=blog), many=True)
        return Response({'blog': BlogSerializer(blog).data, 'comments': comments.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        blog = get_object_or_404(Blog, pk=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        return Response(status=status.HTTP_200_OK)
