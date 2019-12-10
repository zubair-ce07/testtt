from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from social_app.models import Comment, Post, Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image',)
        read_only_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name', 'profile', 'last_name', 'bio', 'image',)


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    def get_token(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(request)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        validated_data.pop('profile', {})
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'token', 'username', 'password', 'first_name', 'profile', 'last_name', 'bio', 'image',)


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


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_comments(self, post):
        comments = Comment.objects.filter(post=post).order_by('-updated_at')
        return CommentListSerializer(comments, many=True, context={'request': post}).data

    def get_author(self, post):
        return UserSerializer(post.author).data

    class Meta:
        model = Post
        fields = ('id', 'author', 'body', 'comments', 'title', 'image', 'created_at', 'updated_at')
