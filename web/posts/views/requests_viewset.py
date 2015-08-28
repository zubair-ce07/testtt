from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Request
from web.posts.serializers.request_serializer import RequestSerializer
from web.users.models import User
from web.users.serializers.user_serializer import UserSerializer


class RequestViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):

    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        kargs = self.kwargs
        return Request.objects.all()
