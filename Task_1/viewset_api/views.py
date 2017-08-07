from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from django.db.models.fields.files import FileField, ImageFieldFile
# from django_countries.fields import Country

from users.models import UserProfile
from viewset_api.serializers import UserSerializer, LoginSerializer, SignupSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
max_age = int(settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA').total_seconds())


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


@api_view(['GET'])
def api_root(request, format=None):
    return Response({'users': reverse('viewset:list', request=request, format=format), }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
        List API: 'viewset_api/list/'

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

        Details API: 'viewset_api/[0-9]+(user_id)/details/'

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
        if request.user.id != int(kwargs.get('pk')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(request.user, serializer.validated_data)
            return super(UserViewSet, self).update(request, *args, **kwargs)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super(UserViewSet, self).destroy(request, *args, **kwargs)
        response = redirect('viewset:login')
        response.delete_cookie('token')
        return response


class Login(viewsets.GenericViewSet):
    """
    API: 'viewset_api/login/'

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
    serializer_class = LoginSerializer

    def retrieve(self, request):
        if request.user.is_authenticated:
            return redirect('viewset:details', pk=request.user.userprofile.id)
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def submit(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data.get('username'),
                                password=serializer.validated_data.get('password'))
            if user and user.is_active:
                response = redirect('viewset:details', pk=user.userprofile.id)
                response.set_cookie('token', get_token(user), max_age=max_age)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signup(viewsets.GenericViewSet):
    """
        API: 'viewset/signup/'

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

    def retrieve(self, request):
        if request.user.is_authenticated:
            return redirect('viewset:details', pk=request.user.id)
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            response = redirect('viewset:details', pk=user.id)
            response.set_cookie('token', get_token(user), max_age=max_age)
            return response
        return Response({'serializer': serializer}, status=status.HTTP_400_BAD_REQUEST)


class Logout(viewsets.GenericViewSet):
    def get(self, request):
        response = redirect('viewset:login')
        response.delete_cookie('token')
        return response
