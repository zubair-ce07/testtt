import json

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Profile
from .serializers import UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer


class UserDirectsView(APIView):
    """
    View to list the complete heirarchy of users starting from the current user
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the heirarchy of users as a recursive JSON object
        """
        response_dict = {
            'user': "",
            'directs': []
        }
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        directs = Profile.objects.filter(supervisor=user).all()
        directs = list(map(lambda x: x.user.username, directs))
        response_dict['user'] = user.username
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)
        pass
