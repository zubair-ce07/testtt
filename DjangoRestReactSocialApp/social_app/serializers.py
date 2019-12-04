from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from rest_framework_jwt.settings import api_settings

from social_app.models import Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name')


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(request)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name',
                  'last_name')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'comment', 'post', 'created_at', 'updated_at')


class CommentListSerializer(CommentSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, comment):
        return UserSerializer(comment.author).data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'body', 'comments', 'title', 'image', 'created_at', 'updated_at')


class PostListSerializer(PostSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_comments(self, post):
        comments = Comment.objects.filter(post=post).order_by('-updated_at')
        return CommentListSerializer(comments, many=True, context={'request': post}).data

    def get_author(self, post):
        return UserSerializer(post.author).data
