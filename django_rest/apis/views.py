from django.contrib.auth import authenticate
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class AuthenticateUser(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(
                {'error': 'Please provide both username and password'},
                status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(response, status=HTTP_200_OK)


class RegisterUser(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
