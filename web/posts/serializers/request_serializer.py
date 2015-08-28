from rest_framework import serializers
from web.posts.models import PostView, Post, Request
from web.posts.serializers.post_serializer import PostSerializer
from web.users.models import User
from web.users.serializers.user_serializer import UserSerializer


class RequestSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(source='requested_by', queryset=User.objects.all())
    post_id = serializers.PrimaryKeyRelatedField(source='post', queryset=Post.objects.all())

    class Meta:
        model = Request
        fields = ('user_id', 'post_id', 'message', 'price', 'requested_on')
