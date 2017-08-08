from rest_framework import viewsets, permissions
from url_crawler.models import CustomUser
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update and delete for user
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
