from rest_framework import views, viewsets, mixins, status, generics
from rest_framework_simplejwt import views as jwt_views
from rest_framework.response import Response

from core import serializers
from core import models


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostMediaViewSet(viewsets.ModelViewSet):
    queryset = models.PostMedia.objects.all()
    serializer_class = serializers.PostMediaSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = models.Following.objects.all()
    serializer_class = serializers.FollowingSerializer


class PostMediaView(generics.ListAPIView):
    queryset = models.PostMedia.objects.all()
    serializer_class = serializers.PostMediaSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(post=pk)
        # context is needed to get full URL
        serializer = self.serializer_class(
            queryset, context={"request": request}, many=True)
        return Response(serializer.data)


class UserPostView(views.APIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(author=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PostCommentView(views.APIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(post=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserFollowingView(views.APIView):
    queryset = models.Following.objects.all()
    serializer_class = serializers.FollowingSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(follower=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FeedView(views.APIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Following.objects.all()

    def get(self, request, user_id):
        followees = [following.followee.id for following in self.queryset.filter(
            follower_id=user_id)]
        followees.append(user_id)
        posts = models.Post.objects.filter(author__in=followees)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationView(views.APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class LoginRefreshView(jwt_views.TokenRefreshView):
    serializer_class = serializers.LoginRefreshSerializer
