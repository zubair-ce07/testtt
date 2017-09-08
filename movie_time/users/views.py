from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User, FollowRequest
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


@api_view(http_method_names=['POST'])
def obtain_auth_token(request):
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


# URL: <host>/users/<receiver_id>/send-request/
@api_view(['POST'])
@permission_classes(permissions.IsAuthenticated)
def send_follow_request(request, receiver_id):
    try:
        receiver = User.objects.get(receiver_id)
    except ObjectDoesNotExist:
        raise exceptions.NotFound()

    request, created = FollowRequest.objects.get_or_create(from_user=request.user, to_user=receiver)
    if not created:
        raise exceptions.ValidationError('Follow request is already sent.')

    return Response({'status': 'sent'})


# URL: <host>/requests/<request_id>/<action[accept or block]>/
@api_view(['PUT'])
@permission_classes(permissions.IsAuthenticated)
def accept_or_block_request(request, request_id, action):
    try:
        request = FollowRequest.objects.get(id=request_id, to_user=request.user)
    except ObjectDoesNotExist:
        raise exceptions.NotFound()

    request.status = FollowRequest.ACCEPTED if action == 'accept' else FollowRequest.BLOCKED
    return Response({'status': 'saved'})
