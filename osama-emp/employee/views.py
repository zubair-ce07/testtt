from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets

from .models import Profile
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
