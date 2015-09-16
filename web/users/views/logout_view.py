import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.users.serializers.profile_serializer import ProfileSerializer


class LogoutView(views.APIView):

    permission_classes = (IsAuthenticated,)

    # noinspection PyMethodMayBeStatic
    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)