from rest_framework import serializers
from web.constants import MUST_BE_NON_NEGATIVE
from web.posts.models import Request


class RequestSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(source='requested_by', read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)
    post_title = serializers.SerializerMethodField(source='get_post_title', read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'user_id', 'post_id', 'post_title', 'message', 'price', 'status', 'requested_on')

    # noinspection PyMethodMayBeStatic
    def get_post_title(self, request):
        return request.post.title

    # noinspection PyMethodMayBeStatic
    def validate_requested_price(self, requested_price):
        if requested_price <= 0.0:
            raise serializers.ValidationError(MUST_BE_NON_NEGATIVE)
        return requested_price
