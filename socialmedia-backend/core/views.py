from rest_framework import views, viewsets, mixins, status, generics
from rest_framework_simplejwt import views as jwt_views
from rest_framework.response import Response

from users.models import FriendList

from core import serializers
from core import models


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects
    serializer_class = serializers.PostSerializer


class PostMediaViewSet(viewsets.ModelViewSet):
    queryset = models.PostMedia.objects
    serializer_class = serializers.PostMediaSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects
    serializer_class = serializers.CommentSerializer


class PostMediaView(generics.ListAPIView):
    queryset = models.PostMedia.objects
    serializer_class = serializers.PostMediaSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(post=pk)
        # context is needed to get full URL
        serializer = self.serializer_class(
            queryset, context={"request": request}, many=True)
        return Response(serializer.data)


class PostCommentView(views.APIView):
    queryset = models.Comment.objects
    serializer_class = serializers.CommentSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(post=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FeedView(views.APIView):
    serializer_class = serializers.PostSerializer
    queryset = FriendList.objects

    def get(self, request, user_id):
        friends = [friendlist.friend.id for friendlist in self.queryset.filter(
            added_by=user_id)]
        friends.append(user_id)
        posts = models.Post.objects.filter(author__in=friends)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
