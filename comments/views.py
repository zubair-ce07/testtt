from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from comments.models import Comment, Follow
from comments.serializers import CommentSerializer, FollowSerializer


class CreateComment(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CreateFollow(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class CommentsList(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FollowsList(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FollowDetail(RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
