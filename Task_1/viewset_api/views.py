from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from task1.permissions import IsOwnerOrReadOnly
from task1.utils import response_json, get_token, get_object
from viewset_api.serializers.auth_serializers import LoginSerializer, SignupSerializer
from viewset_api.serializers.user_serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    List API: 'viewset_api/users/'

    Method: 'GET'

    GET:
    Function name: list
    Response Body: {
        "success": true,
        "message": null,
        "response": [
            {
                "url": "viewset_api/users/<user_id>/",
                "username": "john_doe",
                "email": "john@doe.com",
                "first_name": "John",
                "last_name": "Doe",
                "userprofile": {
                    "phone_number": "+923331234567",
                    "country": "US",
                    "image": "users/john.jpg"/null,
                    "address": "X House, Y Street, Brooklyn, NY 11229"
                }
            }
            {
                ....
            }
            ....
        ]
    }

    Details API: 'viewset_api/users/<user_id>/'

    Methods: 'GET, PUT, PATCH, DELETE'

    GET:
    Function name: retrieve
    Response Body:
    {
        "success": true,
        "message": null,
        "response": {
            "url": "viewset/users/<user_id>/",
            "username": "john_doe",
            "email": "john@doe.com",
            "first_name": "John",
            "last_name": "Doe",
            "userprofile": {
                "phone_number": "+923331234567",
                "country": "US",
                "image": "users/john.jpg"/null,
                "address": "X House, Y Street, Brooklyn, NY 11229"
            }
        }
    }

    PUT, PATCH:
    Function name: update
    Request Body: {
        "email": "john@doe.com",
        "first_name": "John",
        "last_name": "Doe",
        "userprofile": {
            "phone_number": "+923331234567",
            "country": "US",
            image": "UploadedFile:users/john.jpg"/null,
            "address": "X House, Y Street, Brooklyn, NY 11229"
        }
    }

    Response Body: {
        "success": true,
        "message": "User successfully updated",
        "response": {
            "url": "viewset/users/<user_id>/",
            "username": "john_doe",
            "email": "john@doe.com",
            "first_name": "John",
            "last_name": "Doe",
            "userprofile": {
                "phone_number": "+923331234567",
                "country": "US",
                "image": "users/john.jpg"/null,
                "address": "X House, Y Street, Brooklyn, NY 11229"
            }
        }
    }

    DELETE:
    Function name: destroy
    Response Body: {
        "success": True,
        "message='User successfully deleted',
        "response": null,
    }
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)

    @transaction.atomic
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


class LoginViewSet(viewsets.GenericViewSet):
    """
    API: 'viewset_api/login/'

    Method: 'POST'

    POST:
    Function name: post
    Request Body: {
        "username": "john.doe",
        "password": "abcdefgh",
    }

    Response Body: {
        "success": true/false,
        "message": "User successfully logged in"/"Invalid Credentials/User account inactive",
        "response": {
            "username": "john.doe",
            "password": "abcdefgh",
            "token": "JWT token"
        }
    }
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user:
                token = get_token(user)
                serializer.validated_data.update({'token': token})
                response = Response(
                    response_json(True, serializer.validated_data, message='User successfully logged in'),
                    status=status.HTTP_200_OK)
                response.set_cookie('token', token)
                return response
        return Response(response_json(False, serializer.data, message='Invalid credentials/User account inactive'),
                        status=status.HTTP_400_BAD_REQUEST)


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    API: 'viewset_api/signup/'

    Method: 'POST'

    POST:
    Function name: create
    Request Body: {
        "username":"john_doe",
        "password":"abcdefgh"
        "password2":"abcdefgh",
        "email": "john@doe.com",
        "first_name": "John",
        "last_name": "Doe",
        "userprofile": {
            "phone_number": "+923331234567",
            "country": "US",
            image": "UploadedFile:users/john.jpg"/null,
            "address": "X House, Y Street, Brooklyn, NY 11229"
        }
    }

    Response body: {
        "success": true,
        "message": "User successfully created",
        "response": {
            "username":"john_doe",
            "password":"Hashed Password"
            "email": "john@doe.com",
            "first_name": "John",
            "last_name": "Doe",
            "userprofile": {
                "phone_number": "+923331234567",
                "country": "US",
                image": "users/john.jpg"/null,
                "address": "X House, Y Street, Brooklyn, NY 11229"
            },
            "token": "JWT token"
        }
    }
    """

    serializer_class = SignupSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super(SignupViewSet, self).create(request, *args, **kwargs)
        token = get_token(get_object(response.data.get('username')))
        response.data.update({'token': token})
        response = Response(response_json(True, response.data, message='User successfully created'),
                            status=status.HTTP_200_OK)
        response.set_cookie('token', token)
        return response


class LogoutViewSet(viewsets.GenericViewSet):
    """
    API: 'viewset/logout/'

    Method: 'GET'

    GET:
    Function name: get
    Response body: {
        "success": true/false,
        "message": "User successfully logged out.",
        "response": null
    }
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        response = Response(response_json(True, None, message='User successfully logged out.'),
                            status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('token')
        return response
