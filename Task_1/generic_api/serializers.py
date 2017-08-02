from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='generic:details')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password')
        read_only_fields = (
            'id', 'user_permissions', 'date_joined', 'last_login', 'groups', 'is_superuser', 'is_staff', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
