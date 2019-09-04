from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = [
            'is_staff', 'is_superuser', 'is_active', 'password',
            'groups', 'user_permissions', 'last_login'
        ]


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FriendList
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)

    class Meta:
        model = models.User
        exclude = ['is_staff', 'is_superuser']


class LoginSerializer(jwt_serializers.TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _(
            f'The email and password you entered did not match our records.'
            f' Please double-check and try again.'
        )
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_id'] = self.user.id

        return data


class LoginRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    pass
