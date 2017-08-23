from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from task1.utils import get_token, response_json
from api.serializers.auth_serializers import LoginSerializer, SignupSerializer
from api.serializers.user_serializers import UserSerializer


class UserListView(APIView):
    """
    API: 'api/user_list/'

    Method: 'GET'

    GET:
    Function name: get
    Response body: {
        "success": true,
        "message": null,
        "response": [
        {
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
        },
        {
            .....
        }
        .....
        ]
    }
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(response_json(True, serializer.data, message=None), status=status.HTTP_200_OK)


class CreateUserView(APIView):
    """
    API: 'api/user_create/'

    Methods: 'GET, PUT, DELETE'

    GET:
    Function name: get
    Response body: {
        "success": true,
        "message": null,
        "response": {
            "username": "",
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

    PUT:
    Function name: put
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
            "password":"abcdefgh"
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

    def get(self, request):
        serializer = SignupSerializer()
        return Response(response_json(True, serializer.data, message=None), status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token(user)
            serializer.validated_data.update({'token': token})
            response = Response(response_json(True, serializer.validated_data, 'User succesfully created'),
                                status=status.HTTP_200_OK)
            response.set_cookie('token', token)
            return response
        return Response(response_json(False, None, message=serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDeleteUserView(APIView):
    """
    API: 'api/users/'

    Methods: 'GET, PUT, DELETE'

    GET:
    Function name: get
    Response body: {
        "success": true,
        "message": null,
        "response": {
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

    PUT:
    Function name: put
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

    Response body: {
        "success": true,
        "message": null,
        "response": {
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
    Function name: delete
    Response body: {
        "success": true,
        "message": "User succesfully deleted",
        "response": null
    }
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(response_json(True, serializer.data, message=None), status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(response_json(True, serializer.validated_data, 'User successfully updated'),
                            status=status.HTTP_200_OK)
        return Response(response_json(False, None, message=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(response_json(True, None, message='User succesfully deleted'),
                        status=status.HTTP_204_NO_CONTENT)


class UserProfileDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/details.html'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'serializer': serializer.data}, status=status.HTTP_200_OK)


class UpdateUserProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/edit.html'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('api:details')
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/login.html'

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user:
                response = redirect('api:details')
                response.set_cookie('token', get_token(user))
                return response
            else:
                return Response({'serializer': serializer, 'errors': 'Invalid Credentials/User account inactive'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/signup.html'

    def get(self, request):
        return Response({'serializer': SignupSerializer()}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = redirect('api:details')
            response.set_cookie('token', get_token(user))
            return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        response = redirect('api:login')
        response.delete_cookie('token')
        return response
