from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import User
from user_api.permissions import IsOwnerOrReadOnly
from user_api.serializers import UserSerializer


class ObtainAuthToken(APIView):
    """
    API endpoint to obtain token by posting email or phone as
    user identifier and password, to use as authorization header
    """
    def post(self, request):
        """
        Serialize email and password and after successful authentication
        returns token to be used as Auth header in further requests
        Arguments:
            request (Request): post request for obtaining token
        Returns:
            response (Response): Serialized User containing token
        Raises:
            AuthenticationFailed: If user can not be verified for some reason
        """

        try:
            email = request.data['email']
        except KeyError:
            email = None

        try:
            phone = request.data['phone']
        except KeyError:
            phone = None

        if not (email or phone):
            raise exceptions.ParseError('Email-Password or Phone-Password are required.')
        try:
            password = request.data['password']
            user = authenticate(email_or_phone=email or phone, password=password)
        except KeyError:
            raise exceptions.ParseError('Password is required.')

        if not user:
            raise exceptions.AuthenticationFailed('Unable to log in with provided credentials.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User\'s account is not active.', code='authorization')

        # setting user as it is authenticated and serializer will use it serialize token
        request.user = user
        return Response(UserSerializer(user, context={'request': request}).data)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update and delete for user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
