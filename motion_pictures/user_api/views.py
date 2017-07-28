from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import User
from user_api.permissions import IsOwnerOrReadOnly
from user_api.serializers import AuthTokenSerializer, UserSerializer, UserUpdateSerializer


# request methods that can result in updates
UPDATE_METHODS = ('PUT', 'PATCH')


class ObtainAuthToken(APIView):
    """
    API endpoint to obtain token by posting email and
    password, to use as authorization header
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        """
        Serialize email and password and after successful authentication
        returns token to be used as Auth header in further requests
        Arguments:
            request (Request): post request for obtaining token
        Returns:
            response (Response): response containing token
        Raises:
            AuthenticationFailed: if provided credentials are incorrect
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.AuthenticationFailed(msg, code='authorization')

        token = Token.objects.get(user=user)
        return Response({'token': token.key})


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update and delete for user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        """
        returns Serializer depending upon the request
        Returns:
             serializer_class(ModelSerializer): class to serialize request and response data
        """
        serializer_class = self.serializer_class

        if self.request.method in UPDATE_METHODS:
            serializer_class = UserUpdateSerializer

        return serializer_class
