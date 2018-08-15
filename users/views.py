from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from users.serializers import UserSerializer, ProfileSerializer, CreateUserSerializer, LoginInputSerializer
from users.models import Profile
from django.contrib.auth import authenticate, login
import jwt


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CreateUserView(APIView):
    serializer_class = CreateUserSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, format='json'):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data)
            else:
                return Response('Could not create user')


class UserLoginView(APIView):
    serializer_class = LoginInputSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            payload = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            jwt_token = {jwt.encode(payload, "SECRET_KEY")}
            return Response(
                {
                    'token': jwt_token,
                    'user': UserSerializer(user, context={'request': request}).data
                }
            )
        else:
            return Response({'Error': "User not found"}, status="404")
