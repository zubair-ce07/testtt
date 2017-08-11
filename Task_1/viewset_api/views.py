from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.models import UserProfile
from viewset_api.serializers import UserSerializer, LoginSerializer, SignupSerializer, UserProfileSerializer
from viewset_api.utils import response_json, get_token
from viewset_api.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('viewset:list', request=request, format=format), }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
        List API: 'viewset_api/list/'

        Method: 'GET'

        Response Body:
            {
                "success": true,
                "message": null,
                "response": {
                    "url": "http://localhost:8000/viewset_api/[0-9]+/details/",
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

        Details API: 'viewset_api/[0-9]+(user_id)/details/'

        Methods: 'GET, PUT, PATCH, DELETE'

            GET:
                Response Body:
                {
                    "success": true,
                    "message": null,
                    "response": {
                        "url": "http://localhost:8000/viewset_api/[0-9]+/details/",
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
                Response Body:
                {
                    "success": true,
                    "message": "User successfully updated",
                    "response": {
                        "url": "http://localhost:8000/viewset_api/[0-9]+/details/",
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

            DELETE:
            {
                "success": True,
                "message='User successfully deleted',
                "response": null,
            }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

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

    Method: 'GET, POST'
    GET:
    Response Body:
        {
            "success": true,
            "message": null,
            "response": {
                "username": "",
                "password": ""
            }
        }
    POST:
    Response Body:
    {
        "success": true,
        "message": "User has been logged in",
        "response": {
            "username": "fakhar",
            "password": "csgogodancer",
            "token": "JWT token"
        }
    }
    """
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = LoginSerializer

    def get(self, request):
        serializer = self.serializer_class()
        return Response(response_json(True, serializer.data, None), status=status.HTTP_200_OK)

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
        return Response(response_json(False, serializer.data, message='Invalid credentials'),
                        status=status.HTTP_400_BAD_REQUEST)


class Signup(viewsets.GenericViewSet):
    """
        API: 'viewset_api/signup/'

        Method: 'GET, POST'

        GET:
        Response body:
        {
            "success": true,
            "message": null,
            "response": {
                "username": "",
                "password": "",
                "password2": "",
                "email": "",
                "first_name": "",
                "last_name": "",
                "userprofile": {
                    "phone_number": "",
                    "country": null,
                    "image": null,
                    "address": ""
                }
            }
        }

        POST:
        Response Body:
        {
            "success": true/false,
            "message": null/'User has been successfully created',
            "response": {
                "token":"JWT Token"
            }
        }
        """
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = SignupSerializer

    def get(self, request):
        serializer = self.serializer_class()
        return Response(response_json(True, serializer.data, None), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token(user)
            response = Response(
                response_json(True, {'token': token}, message='User has been successfully created'),
                status=status.HTTP_200_OK)
            response.set_cookie('token', token)
            return response


class Logout(viewsets.GenericViewSet):
    """
    API: 'viewset/logout/'

        Method: 'GET'

        GET:
        Response body:
        {
            "success": true/false,
            "message": "User has been successfully logged out."/ "No user logged in to log out.",
            "response": null
        }
    """

    def get(self, request):
        if request.user.is_authenticated:
            response = Response(response_json(True, None, message='User has been successfully logged out.'),
                                status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie('token')
            return response
        return Response(response_json(False, None, message='No user logged in to log out.'),
                        status=status.HTTP_400_BAD_REQUEST)
