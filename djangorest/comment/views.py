from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from comment.serializers import CommentSerializer
from comment.models import Comment
from rest_framework import permissions


"""
    This view handles the creation of new comments on a blog.
"""


class CommentCreate(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        form_data = request.POST.copy()
        form_data.update({'created_by': request.user})
        print (form_data)
        serializer = CommentSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDelete(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_200_OK)
