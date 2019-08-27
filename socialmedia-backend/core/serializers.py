from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Post, Comment, Following


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name',
                  'last_name', 'email', 'display_picture']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'time', 'status']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post' 'author', 'time', 'message']


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['id', 'follower', 'followee']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'token']


class LoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': _('The username and password you entered did not match our records. Please double-check and try again.')
    }

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_id'] = self.user.id

        return data

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)

#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)

#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.')
#         if password is None:
#             raise serializers.ValidationError(
#                 'Password is required to log in.')

#         user = authenticate(username=email, password=password)

#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )

#         return {
#             'email': user.email,
#             'token': user.token
#         }
