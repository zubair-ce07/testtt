from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import User
from user_api.permissions import IsOwnerOrReadOnly
from user_api.serializers import UserSerializer


class ObtainAuthToken(APIView):
    """
    API endpoint to obtain token by posting email and
    password, to use as authorization header
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
            email_or_phone = request.data['user']
            password = request.data['password']
            user = authenticate(email_or_phone=email_or_phone, password=password)
        except KeyError:
            msg = 'Email or Phone (as user) and Password are required.'
            raise exceptions.AuthenticationFailed(msg, code='authorization')

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.AuthenticationFailed(msg, code='authorization')

        if not user.is_active:
            msg = 'User\'s account is not active.'
            raise exceptions.AuthenticationFailed(msg, code='authorization')

        request.user = user
        return Response(UserSerializer(user, context={'request': request}).data)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update and delete for user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
