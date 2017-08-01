from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from user.serializers import UserSerializer


class APILogin(APIView):

    username = None
    password = None

    def post(self, request, format=None):
        print(request.data)
        self.username = request.data.get('username', None)
        self.password = request.data.get('password', None)
        requested_user = authenticate(username=self.username, password=self.password)
        if requested_user:
            user_token, is_created = Token.objects.get_or_create(user=requested_user)
            return Response(data={'data': 'User Logged In', 'token': user_token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class APISignUp(APIView):

    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        print(request.data)
        profile = UserSerializer(data=request.data)
        if profile.is_valid():
            profile.save()
            return Response(data={'data': 'User Created'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'data': profile.errors}, status=status.HTTP_400_BAD_REQUEST)
