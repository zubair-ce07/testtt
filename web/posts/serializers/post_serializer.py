from django.utils import timezone
from rest_framework import serializers
from web.posts.models import Post
from web.users.models import Address
from web.users.serializers.address_serializer import AddressSerializer


class PostSerializer(serializers.HyperlinkedModelSerializer):

    location = AddressSerializer()
    user_id = serializers.PrimaryKeyRelatedField(source='posted_by', read_only=True)
    number_of_views = serializers.SerializerMethodField(source='get_number_of_views', read_only=True)
    is_sold = serializers.BooleanField(read_only=True)
    time_until_expired = serializers.SerializerMethodField(source='get_time_until_expired', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'title', 'area', 'location', 'description', 'kind', 'number_of_views',
                  'contact_number', 'demanded_price', 'expired_on', 'is_sold', 'time_until_expired')

    # noinspection PyMethodMayBeStatic
    def get_number_of_views(self, post):
        return post.number_of_views

    # noinspection PyMethodMayBeStatic
    def get_time_until_expired(self, post):
        return post.time_until_expired

    # noinspection PyMethodMayBeStatic
    def validate_title(self, title):
        if len(title) < 5:
            raise serializers.ValidationError('Title is too short elaborate more!')
        return title

    # noinspection PyMethodMayBeStatic
    def validate_area(self, area):
        if area <= 0.0:
            raise serializers.ValidationError('Area must be non-negative!')
        return area

    # noinspection PyMethodMayBeStatic
    def validate_expired_on(self, expired_on):
        time_delta = expired_on - timezone.now()
        if time_delta.total_seconds() < 0:
            raise serializers.ValidationError('give valid expiry time for your post')
        return expired_on

    # noinspection PyMethodMayBeStatic
    def validate_demand(self, demand):
        if demand <= 0.0:
            raise serializers.ValidationError('Demanded price must be non-negative!')
        return demand

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        post = Post.objects.create(location=Address.objects.create(**location_data), **validated_data)
        return post
