from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField, ImageFieldFile
from django.shortcuts import redirect
from django_countries.fields import Country
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from generic_api.serializers import UserSerializer, SignupSerializer, LoginSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
max_age = int(settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA').total_seconds())


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('generic:list', request=request, format=format), }, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    """
      API: 'generic_api/[0-9]+(user_id)/details/'

      Method: 'GET'

      Response Body:
        [
            {
            "url": "generic_api/[0-9]+(user_id)/details/",
            "username": "username",
            "email": "email address",
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone_number": "Phone number with at least 9 numbers",
            "country": "2 digit country code",
            "image": "path for image file on server",
            "address": "Address"
            }
            {
            .......
            }
            .....
        ]
          """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        API: 'generic_api/[0-9]+(user_id)/details/'

        Methods: 'GET, PUT, PATCH, DELETE'

        GET:
        Response Body:
        {
        "url": "generic_api/[0-9]+(user_id)/details/",
        "username": "username",
        "email": "email address",
        "first_name": "First Name",
        "last_name": "Last Name",
        "phone_number": "Phone number with at least 9 numbers",
        "country": "2 digit country code",
        "image": "path for image file on server",
        "address": "Address"
        }

        PUT, PATCH:
        Response Body:
        {
        "url": "generic_api/[0-9]+(user_id)/details/",
        "username": "username",
        "email": "email address",
        "first_name": "First Name",
        "last_name": "Last Name",
        "phone_number": "Phone number with at least 9 numbers",
        "country": "2 digit country code",
        "image": "path for image file on server",
        "address": "Address"
        }

        DELETE:
        {
            Redirect to login page
        }
      """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if request.user.id != int(kwargs.get('pk')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
        return super(UserDetails, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super(UserDetails, self).destroy(request, *args, **kwargs)
        response = redirect('generic:login')
        response.delete_cookie('token')
        return response


class Login(APIView):
    """
    API: 'generic_api/login/'

    Method: 'GET, POST'
    GET:
    Response Body:
        {
            "username": "",
            "password": ""
        }
    POST:
    Response Body:
    {
        Redirect to details page
    }
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('generic:details', pk=request.user.id)
        serializer = LoginSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                response = redirect('generic:details', pk=user.id)
                response.set_cookie('token', get_token(user), max_age=max_age)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signup(generics.CreateAPIView):
    """
    API: 'generic_api/signup/'

    Method: 'GET, POST'

    GET:
    Response body:
    {
    "username": "",
    "password": "",
    "password2": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "phone_number": "",
    "country": "",
    "image": file upload button,
    "address": ""
    }

    POST:
    {
    Either same data with errors or redirect to user details page
    username": "",
    "password": "",
    "password2": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "phone_number": "",
    "country": "",
    "image": file upload button,
    "address": ""
    }
    """
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('generic:details', pk=request.user.id)
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            response = redirect('generic:details', pk=user.id)
            response.set_cookie('token', get_token(user), max_age=max_age)
            return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def get(self, request):
        response = redirect('generic:login')
        response.delete_cookie('token')
        return response
