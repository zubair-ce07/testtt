from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.users.models import User
from web.users.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        self.queryset = User.objects.filter(pk=self.request.user.id)
        return self.queryset
