from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.Serializers.user_serializer import UserSerializer


class UserViewSet(ViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            new_group, created = Group.objects.get_or_create(
                name=request.data['group'])
            user.groups.set([new_group])
            json = dict()
            json['result'] = "success"

        return Response(json, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
