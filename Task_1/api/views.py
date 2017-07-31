from rest_framework import generics
from django.contrib.auth.models import User

from users.models import UserProfile
from api.serializers import UserSerializer, UserProfileSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
