from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Request
from web.posts.serializers.request_serializer import RequestSerializer


class MyRequestsViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Request.objects.filter(requested_by=self.request.user)




