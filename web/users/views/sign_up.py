from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.users.models import User
from web.users.permissions import IsEligible
from web.users.serializers.user_serializer import UserSerializer


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = (IsEligible,)