from rest_framework import generics

from ..models import User
from .serliazers import UserSerializer
from .permissions import isAdminOrReadOnly, isSameUser


class UserApi(generics.ListCreateAPIView):
    """Rest api for users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (isAdminOrReadOnly, )


class UserDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """Rest api for a single user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (isAdminOrReadOnly, isSameUser)
