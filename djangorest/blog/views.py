from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Blog
from blog.serializers import BlogSerializer
from django.shortcuts import get_object_or_404


class APIBlogList(APIView):

    def get(self, request, format=None):
        return Response(BlogSerializer(Blog.objects.all(), many=True).data, status=status.HTTP_200_OK)


class APIBlogDetail(APIView):

    def get(self, request, pk, format=None):
        blog = get_object_or_404(Blog, pk=pk)
        return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)

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
        return Response(status=status.HTTP_204_NO_CONTENT)
