from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.users.serializers.change_password_serializer import ChangePasswordSerializer


class ChangePasswordViewSet(mixins.CreateModelMixin, GenericViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return ChangePasswordSerializer(self.request.user, *args, **kwargs)
