from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from rest_framework import viewsets, permissions, exceptions, response, parsers
from rest_framework.decorators import api_view
from url_crawler.models import CustomUser
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update and delete for user
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,)


def logout_user(request):
    logout(request)
    return redirect('users:login')


@api_view(['POST'])
def login_user(request):
    """
    Serialize email and password and after successful authentication user is logged in

    Arguments:
        request (Request): post request for login
    Returns:
        response (Response): Serialized User
    Raises:
        AuthenticationFailed: If user can not be verified for some reason
    """

    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        raise exceptions.ParseError('Email and Password are required.')

    user = authenticate(email=email, password=password)
    if not user:
        raise exceptions.AuthenticationFailed('Unable to log in with provided credentials.')
    if not user.is_active:
        raise exceptions.AuthenticationFailed('User\'s account is not active.')
    login(request, user)
    return response.Response(UserSerializer(user, context={'request': request}).data)
