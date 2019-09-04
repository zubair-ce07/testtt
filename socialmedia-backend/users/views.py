from rest_framework import views, viewsets, mixins, status, generics
from rest_framework_simplejwt import views as jwt_views
from rest_framework.response import Response

from core.models import Post
from core.serializers import PostSerializer
from users import models
from users import serializers


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = models.User.objects
    serializer_class = serializers.UserSerializer


class FriendListViewSet(viewsets.ModelViewSet):
    queryset = models.FriendList.objects
    serializer_class = serializers.FriendListSerializer


class UserPostView(views.APIView):
    queryset = Post.objects
    serializer_class = PostSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(author=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserFriendListView(views.APIView):
    queryset = models.FriendList.objects
    serializer_class = serializers.FriendListSerializer

    def get(self, request, pk):
        queryset = self.queryset.filter(added_by=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class LoginView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class LoginRefreshView(jwt_views.TokenRefreshView):
    serializer_class = serializers.LoginRefreshSerializer


class RegistrationView(views.APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
