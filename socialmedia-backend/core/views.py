from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import views, viewsets, mixins, status
from rest_framework.viewsets import generics

from . import serializers
from . import models


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """ API endpoint that allows users to be viewed or edited """
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class PostAPIView(generics.GenericAPIView, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def post(self, request):
        return self.create(request)

    def delete(self, request, pk):
        return self.destroy(request)

    def get(self, request):
        author = self.request.query_params.get('author', None)
        queryset = self.queryset.filter(author=author)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CommentAPIView(generics.GenericAPIView, mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def post(self, request):
        return self.create(request)

    def delete(self, request):
        return self.destroy(request)

    def get(self, request):
        post = self.request.query_params.get('post', None)
        queryset = self.queryset.filter(post=post)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FollowingAPIView(generics.GenericAPIView, mixins.CreateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = models.Following.objects.all()
    serializer_class = serializers.FollowingSerializer

    def post(self, request):
        return self.create(request)

    def delete(self, request):
        return self.destroy(request)

    def get(self, request):
        follower_id = self.request.query_params.get('follower_id', None)
        print("Follower ID", follower_id)

        if follower_id:
            queryset = self.queryset.filter(follower_id=follower_id)
        else:
            queryset = self.queryset

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FeedAPIView(views.APIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Following.objects.all()

    def get(self, request, user_id):
        followees = [following.followee.id for following in self.queryset.filter(
            follower_id=user_id)]
        followees.append(user_id)
        posts = models.Post.objects.filter(author__in=followees)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user = request.data

        print(user)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print("sersse", serializer.validated_data)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    #     permission_classes = [AllowAny]
    #     serializer_class = LoginSerializer

    #     def post(self, request):
    #         user = request.data

    #         serializer = self.serializer_class(data=user)
    #         serializer.is_valid(raise_exception=True)

    #         return Response(serializer.data, status=status.HTTP_200_OK)
