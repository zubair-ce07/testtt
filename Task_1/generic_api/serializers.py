from rest_framework import serializers

from users.serializers.user_serializers import UserSerializer as uSerializer


class UserSerializer(uSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')
