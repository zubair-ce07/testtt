from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.serializers.auth_serializers import LoginSerializer, SignupSerializer
from api.serializers.user_serializers import UserSerializer
from task1.utils import get_token, response_json


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('api:list', request=request, format=format)}, status=status.HTTP_200_OK)


class UserListAPI(APIView):
    """
    API: 'api/list_api/'

    Method: 'GET'

    GET:
    Response body: {
        "success": true,
        "message": null,
        "response": [
        {
            "username": "username",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/image.jpg",
                "address": "Address"
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

    def get(self, request, format=None):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(response_json(True, serializer.data, message=None), status=status.HTTP_200_OK)


class RetrieveUpdateDeleteUserProfile(APIView):
    """
    API: 'api/details_api/'

    Methods: 'GET, PUT, DELETE'

    GET:
    Response body: {
        "success": true,
        "message": null,
        "response": {
            "username": "Username",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "media/users/image.jpg",
                "address": "Address"
            }
        }
    }

    PUT:
    Request Body: {
        "email": "Email Address",
        "first_name": "First Name",
        "last_name": "Last Name",
        "userprofile.phone_number": "(+)123456789",
        "userprofile.country": "AZ",
        "userprofile.image": "users/image.jpg",
        "userprofile.address": "Address"
    }

    Response body: {
        "success": true,
        "message": null,
        "response": {
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "userprofile": {
                "phone_number": "(+)1234567891",
                "country": "AZ",
                "image": "users/image.jpg"/null,
                "address": "Address"
            }
        }
    }

    DELETE: {
        "success": true,
        "message": "User has been succesfully deleted",
        "response": null
    }
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(response_json(True, serializer.data, message=None), status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(response_json(False, serializer.data, message=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        request.user.delete()
        return Response(response_json(True, None, message='User has been succesfully deleted'),
                        status=status.HTTP_204_NO_CONTENT)


class UserProfileDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/details.html'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'serializer': serializer.data}, status=status.HTTP_200_OK)


class UpdateUserProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/edit.html'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return redirect('api:details')
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/signup.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('api:details')
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


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/login.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                response = redirect('api:details')
                token = get_token(user)
                response.set_cookie('token', token)
                return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        response = redirect('api:login')
        response.delete_cookie('token')
        return response
