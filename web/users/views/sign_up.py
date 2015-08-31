from rest_framework.generics import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from web.users.serializers.user_serializer import UserSerializer


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)