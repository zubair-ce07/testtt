from rest_framework import views, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (UserSerializer, PostSerializer, CommentSerializer,
                          FollowingSerializer, RegistrationSerializer,
                          LoginSerializer)
from .models import User, Post, Comment, Following


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """ API endpoint that allows users to be viewed or edited """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows posts to be viewed or edited """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows comments to be viewed or edited """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FollowingViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows followings to be viewed or edited """
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer


class RegistrationAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class LoginAPIView(views.APIView):
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data

#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
