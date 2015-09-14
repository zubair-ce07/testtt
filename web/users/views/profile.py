
from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from web.users.models import User
from web.users.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(pk=self.request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)