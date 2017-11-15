from django.contrib.auth.models import User
from rest_framework import serializers
from YouTube.models import Video


class UserSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Video.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'videos')
    # class Meta:
    #     model = User
    #     fields = ('id', 'username', 'email', 'channel')


# class ChannelSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Channel
#         fields = ('id', 'owner', 'subscriber')


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Video
        fields = ('id', 'name', 'owner')