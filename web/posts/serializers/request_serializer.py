from rest_framework import serializers
from web.posts.models import Request


class RequestSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(source='requested_by', read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'user_id', 'post_id', 'message', 'price', 'status', 'requested_on')

    # noinspection PyMethodMayBeStatic
    def validate_requested_price(self, requested_price):
        if requested_price <= 0.0:
            raise serializers.ValidationError('Price must be non-negative!')
        return requested_price
