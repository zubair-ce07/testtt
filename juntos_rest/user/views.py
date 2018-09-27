from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response

from .permissions import StaffPermission, NotLoggedIn
from .serializers import ProfileSerializer, UserRegisterSerializer
from .models import Profile


class ProfileView(RetrieveUpdateAPIView):
    """
    This viewset provides `profile-data` and allows to `update` it.
    """
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class RegisterApiView(CreateAPIView):
    """
    This viewset register new user
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, NotLoggedIn)


class UserListApiView(ListAPIView):
    """
    List all users if admin
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated, StaffPermission)
