from rest_framework import serializers

from users.serializers.user_serializers import UserSerializer as GenericUserSerializer


class UserSerializer(GenericUserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')
