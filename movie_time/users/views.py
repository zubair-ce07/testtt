from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


class ObtainAuthToken(APIView):
    """
    API endpoint to obtain token by posting email and password
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

        email = request.data.get('email')
        password = request.data.get('password')

        if not (email or password):
            raise exceptions.ParseError('Email & Password are required.')

        user = authenticate(email=email, password=password)

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
