from rest_framework import serializers
from web.posts.models import PostView
from web.posts.serializers.post_serializer import PostSerializer
from web.users.serializers.user_serializer import UserSerializer


class PostViewSerializer(serializers.HyperlinkedModelSerializer):

    viewed_by = UserSerializer(many=True)
    post_viewed = PostSerializer()

    class Meta:
        model = PostView
        fields = {'viewed_by', 'post_viewed', 'viewed_on'}