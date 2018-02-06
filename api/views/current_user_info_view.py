from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.Serializers.user_serializer import UserSerializer
from django.shortcuts import get_object_or_404


class CurrentUserInfoView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return user

    def get_object(self):
        return self.request.user
