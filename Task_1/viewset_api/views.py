from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from task1.permissions import IsOwnerOrReadOnly
from viewset_api.serializers.auth_serializers import LoginSerializer, SignupSerializer
from viewset_api.serializers.user_serializers import UserSerializer
from viewset_api.utils import response_json, get_token


class UserViewSet(viewsets.ModelViewSet):
    """
    List API: 'viewset_api/users/'

    Method: 'GET'

    Response Body: {
        "success": true,
        "message": null,
        "response": {
            "url": "http://localhost:8000/viewset_api/users/<user_id>/",
            "username": "username",
            "email": "email address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/user.jpg",
                "address": "Address"
            }
        }
        {
            ......
        }
        .......
    }

    Details API: 'viewset_api/users/<user_id>/'

    Methods: 'GET, PUT, PATCH, DELETE'

    GET:
    Response Body: {
        "success": true,
        "message": null,
        "response": {
            "url": "http://localhost:8000/viewset_api/users/<user_id>/",
            "username": "username",
            "email": "email address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/user.jpg",
                "address": "Address"
            }
        }
    }

    PUT, PATCH:
    Response Body: {
        "success": true,
        "message": "User successfully updated",
        "response": {
            "url": "http://localhost:8000/viewset_api/users/<user_id>/",
            "username": "username",
            "email": "email address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/user.jpg",
                "address": "Address"
            }
        }
    }

    DELETE: {
        "success": True,
        "message='User successfully deleted',
        "response": null,
    }
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def list(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        response = super(UserViewSet, self).update(request, *args, **kwargs)
        return Response(response_json(True, response.data, message='User successfully updated'),
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super(UserViewSet, self).destroy(request, *args, **kwargs)
        response = Response(response_json(True, None, message='User successfully deleted'),
                            status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('token')
        return response


class Login(viewsets.GenericViewSet):
    """
    API: 'viewset_api/login/'

    Method: 'POST'

    POST:
    Response Body: {
        "success": true/false,
        "message": "User has been logged in"/"Invalid Credentials",
        "response": {
            "username": "username",
            "password": "password",
            "token": "JWT token"
        }
    }
    """

    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                token = get_token(user)
                serializer.validated_data.update({'token': token})
                response = Response(response_json(True, serializer.validated_data, message='User has been logged in'),
                                    status=status.HTTP_200_OK)
                response.set_cookie('token', token)
                return response
            else:
                return Response(response_json(False, serializer.validated_data, message='User account inactive'),
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(response_json(False, serializer.data, message='Invalid credentials'),
                        status=status.HTTP_400_BAD_REQUEST)


class Signup(CreateModelMixin, viewsets.GenericViewSet):
    """
    API: 'viewset_api/signup/'

    Method: 'POST'

    POST:
    Response Body: {
        "success": true,
        "message": "User has been successfully created",
        "response": {
            "username": "Username",
            "password": "Hashed Password",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/image.jpg",
                "address": "Address"
            },
            "token": "JWT Token"
        }
    }
    """

    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = SignupSerializer

    def get_object(self, username):
        return User.objects.get(username=username)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super(Signup, self).create(request, *args, **kwargs)
        token = get_token(self.get_object(response.data.get('username')))
        response.data.update({'token': token})
        response = Response(response_json(True, response.data, message='User has been successfully created'),
                            status=status.HTTP_200_OK)
        response.set_cookie('token', token)
        return response


class Logout(viewsets.GenericViewSet):
    """
    API: 'viewset/logout/'

    Method: 'GET'

    GET:
    Response body: {
        "success": true/false,
        "message": "User has been successfully logged out.",
        "response": null
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = Response(response_json(True, None, message='User has been successfully logged out.'),
                            status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('token')
        return response
