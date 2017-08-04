import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from api.serializers.edit_serializer import EditSerializer
from api.serializers.signup_serializer import SignupSerializer
from api.serializers.user_serializers import UserListSerializer, LoginSerializer
from users.models import UserProfile

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
max_age = int(settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA').total_seconds())


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def refresh_token(request, response):
    token = request.COOKIES.get('token')
    expire = datetime.datetime.fromtimestamp(jwt_decode_handler(token).get('exp'))
    delta = datetime.datetime.now() + datetime.timedelta(hours=1)
    if expire < delta:
        response.set_cookie('token', get_token(request.user), max_age=max_age)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('api:list', request=request, format=format)}, status=status.HTTP_200_OK)


class UserList(APIView):
    """
     API: 'api/list/'

     Method: 'GET, POST'

     Response body:
     {
        "email": "a@b.com",
        "username": "user",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "(+)1234567891",
        "country": "Pakistan",
        "image": "media/users/image.jpg",
        "address": "Address"
    },
    .....
     """

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
        API: 'api/detail/'

        Method: 'GET, PUT, DELETE'
        GET:
        Response body:
         {
            "email": "a@b.com",
            "username": "user",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "(+)1234567891",
            "country": "Pakistan",
            "image": "media/users/image.jpg",
            "address": "Address"
        }
        PUT:
        Response body:
         {
            "email": "a@b.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "(+)1234567891",
            "country": "Select from drop down",
            "image": "File upload button",
            "address": "Address"
        }
        DELETE:
        {
            Redirect to other page
        }
         """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserListSerializer(request.user.userprofile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = UserListSerializer(request.user.userprofile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/details.html'
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserListSerializer(UserProfile.objects.get(user=request.user))
        response = Response({'serializer': serializer.data}, status=status.HTTP_200_OK)
        refresh_token(request, response)
        return response


class UserProfileEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/edit.html'
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = EditSerializer(user_profile)
        response = Response({'serializer': serializer}, status=status.HTTP_200_OK)
        refresh_token(request, response)
        return response

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = EditSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            user_profile = serializer.save()
            response = redirect('api:details')
            response.set_cookie('token', get_token(user_profile.user), max_age=max_age)
            return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/login.html'
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('api:details')
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
                response.set_cookie('token', token, max_age=max_age)
                return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        response = redirect('api:login')
        response.delete_cookie('token')
        return response
