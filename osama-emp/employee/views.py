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

    def make_direct(self, user):
        direct_dict = {}
        direct_dict['username'] = user.username
        direct_dict['job_title'] = user.profile.job_title
        return direct_dict

    def get(self, request, pk, *args, **kwargs):
        """
        Returns the directs of the current user
        """
        response_dict = {
            'user': "",
            'directs': []
        }
        user = User.objects.get(pk=pk)
        directs = User.objects.filter(profile__supervisor=user).all()
        directs = list(map(lambda x: UserSerializer(x).data, directs))
        response_dict['user'] = UserSerializer(user).data
        response_dict['directs'] = directs
        return Response(response_dict, status=status.HTTP_200_OK)
        pass
