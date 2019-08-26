from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
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
        fields = ['id', 'follower_id', 'followee_id']


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
