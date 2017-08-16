from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from user.serializers import UserSerializer


"""
    This view handles the credential validation for a user.
"""


class Login(APIView):

    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return Response(data={'data': 'Params are missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            user_token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'data': 'User Logged In', 'token': user_token.key}, status=status.HTTP_200_OK)
        return Response(data={'data': 'Invalid Username or Password'}, status=status.HTTP_404_NOT_FOUND)


"""
    This view handles the creation of new user.
"""


class APISignUp(APIView):

    def post(self, request, format=None):
        profile = UserSerializer(data=request.data)
        if profile.is_valid():
            profile.save()
            return Response(data={'data': 'User Created'}, status=status.HTTP_200_OK)
        return Response(data={'data': profile.errors}, status=status.HTTP_400_BAD_REQUEST)


"""
    This view handles the logout of users.
"""


class APILogout(APIView):

    def get(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except AttributeError:
            pass
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
