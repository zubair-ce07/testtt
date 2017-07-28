from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from comment.models import Comment
from comment.serializers import CommentSerializer
from django.shortcuts import get_object_or_404


class APICommentList(APIView):

    def get(self, request, format=None):
        print(Comment.objects.all())
        return Response(CommentSerializer(Comment.objects.all(), many=True).data, status=status.HTTP_200_OK)


class APICommentDetail(APIView):

    def get(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
