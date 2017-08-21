from django.contrib.auth import login, logout, authenticate

from rest_framework import generics
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from instagram.serializers import *


class NewsfeedListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    # query_set = Post.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(user=user)
        all_following = FollowRelation.objects.filter(follower__username=user.username).values('user')
        for item in all_following:
            pk = item['user']
            user = User.objects.get(pk=pk)
            posts = posts | Post.objects.filter(user__username=user.username)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class UserLogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({})


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            serializer = UserLoginSerializer(request.data)
            user = authenticate(**serializer.data)
            login(request, user)

            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)



class UserSignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.initial_data['username']
        first_name = serializer.initial_data['first_name']
        last_name = serializer.initial_data['last_name']
        email = serializer.initial_data['email']
        password = serializer.initial_data['password']
        date_of_birth = serializer.initial_data['date_of_birth']
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            password=password,
        )
        # user = User(
        #     username=username,
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email,
        #     date_of_birth=date_of_birth,
        # )
        # user.save()
        # user.set_password(password)
        # user.save()
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameEmailAvailableAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            is_taken = User.objects.filter(username=username).exists()
        except KeyError:
            email = request.data['email']
            is_taken = User.objects.filter(email=email).exists()
        return Response(is_taken)


class UserListAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class LikeListAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
