from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models.fields.files import FileField, ImageFieldFile
from django_countries.fields import Country
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from generic_api.serializers.signup_serializer import SignupSerializer
from generic_api.serializers.user_serializers import UserSerializer, LoginSerializer
from viewset_api.permissions import IsOwnerOrReadOnly
from viewset_api.utils import get_token, response_json


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('generic:list', request=request, format=format), }, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    """
    API: 'generic_api/list/'

    Method: 'GET'

    Response Body:
    {
        "success": true,
        "message": null,
        "response": [
            {
                "url": "generic_api/[0-9]+/details/",
                "username": "Username",
                "email": "Email Address",
                "first_name": "First Name",
                "last_name": "Last Name",
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/image.jpg",
                "address": "Address"
            }
            {
                ....
            }
            ....
            ]
          """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        response = super(UserList, self).list(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    API: 'generic_api/[0-9]+/details/'

    Methods: 'GET, PUT, PATCH, DELETE'

    GET:
    Response Body:
    {
        "success": true,
        "message": null,
        "response": [
            {
                "url": "generic_api/[0-9]+/details/",
                "username": "Username",
                "email": "Email Address",
                "first_name": "First Name",
                "last_name": "Last Name",
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/image.jpg",
                "address": "Address"
            }

    PUT, PATCH:
    Response Body:{
        "success": true,
        "message": "User has been successfully updated",
        "response": [
            {
                "url": "generic_api/[0-9]+/details/",
                "username": "Username",
                "email": "Email Address",
                "first_name": "First Name",
                "last_name": "Last Name",
                "phone_number": "(+)123456789",
                "country": "AZ",
                "image": "users/image.jpg",
                "address": "Address"
            }


        DELETE:
        Response Body:
            {
                "success": True,
                "message='User successfully deleted',
                "response": null,
            }
    }
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        response = super(UserDetails, self).retrieve(request, *args, **kwargs)
        return Response(response_json(True, response.data, message=None), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if not request.data._mutable:
            request.data._mutable = True
        user_profile = request.user.userprofile
        user_profile.phone_number = request.data.dict().get('phone_number')
        request.data.pop('phone_number')
        user_profile.country = Country(code=request.data.dict().get('country'))
        request.data.pop('country')
        user_profile.address = request.data.dict().get('address')
        request.data.pop('address')
        image = request.data.dict().get('image')
        request.data.pop('image')
        if image:
            path = default_storage.save('users/' + image.name, ContentFile(image.read()))
            image = ImageFieldFile(instance=user_profile, field=FileField(), name=path)
            user_profile.image = image
        user_profile.save()
        response = super(UserDetails, self).update(request, *args, **kwargs)
        return Response(response_json(True, response.data, message='User has been successfully updated'),
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = super(UserDetails, self).destroy(request, *args, **kwargs)
        response.delete_cookie('token')
        return Response(response_json(True, response.data, message='User has been succesfully deleted'),
                        status=status.HTTP_204_NO_CONTENT)


class Login(generics.GenericAPIView):
    """
    API: 'generic_api/login/'

    Method: 'GET, POST'

    GET:
    Response Body: {
        "success": true,
        "message": null,
        "response": {
            "username": "",
            "password": ""
        }
    }
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

    def get(self, request):
        serializer = self.serializer_class()
        return Response(response_json(True, serializer.data, None), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
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


class Signup(generics.CreateAPIView):
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
            "phone_number": "",
            "country": null,
            "image": null,
            "address": ""
        }
    }

    POST:
    Response Body:
    {
        "success": true,
        "message": "User has been successfully created",
        "response": {
            "username": "Username",
            "password": "Hashed Password",
            "email": "Email Address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone_number": "(+)123456789",
            "country": "AZ",
            "image": "users/image.jpg",
            "address": "Address"
            "token": "JWT Token"
        }
    }
        """
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = SignupSerializer

    def get_object(self, username):
        return User.objects.get(username=username)

    def get(self, request):
        serializer = self.serializer_class()
        return Response(response_json(True, serializer.data, None), status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super(Signup, self).create(request, *args, **kwargs)
        token = get_token(self.get_object(response.data.get('username')))
        response.data.update({'token': token})
        response = Response(response_json(True, response.data, message='User has been successfully created'),
                            status=status.HTTP_200_OK)
        response.set_cookie('token', token)
        return response


class Logout(APIView):
    """
    API: 'generic_api/logout/'

    Method: 'GET'

    GET:
    Response body:
    {
        "success": true/false,
        "message": "User has been successfully logged out."/ "No user logged in to log out.",
        "response": null
    }
   """
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            response = Response(response_json(True, None, message='User has been successfully logged out.'),
                                status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie('token')
            return response
        return Response(response_json(False, None, message='No user logged in to log out.'),
                        status=status.HTTP_400_BAD_REQUEST)
