from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name',
                  'last_name', 'email', 'display_picture']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'author', 'time', 'status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'post', 'author', 'time', 'message']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Following
        fields = ['id', 'follower', 'followee']


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
        fields = ['email', 'first_name', 'last_name',
                  'password', 'token', 'display_picture']


class LoginSerializer(TokenObtainPairSerializer):
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
