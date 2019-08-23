from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import User
from .serliazers import UserSerializer
from .permissions import isSameUser


class UserApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, )


class UserDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for a single user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, isSameUser)
