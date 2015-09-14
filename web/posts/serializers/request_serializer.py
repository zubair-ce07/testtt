from rest_framework import serializers
from web.constants import MUST_BE_NON_NEGATIVE
from web.posts.models import Request


class RequestSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(source='requested_by', read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)
    post_title = serializers.SerializerMethodField(source='get_post_title', read_only=True)
    posted_by_full_name = serializers.SerializerMethodField(source='get_posted_by_full_name', read_only=True)
    requested_by_full_name = serializers.SerializerMethodField(source='get_requested_by_full_name', read_only=True)
    requested_on = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'user_id', 'post_id', 'posted_by_full_name', 'requested_by_full_name', 'post_title', 'message',
                  'price', 'status', 'requested_on')

    # noinspection PyMethodMayBeStatic
    def get_post_title(self, request):
        return request.post.title

    # noinspection PyMethodMayBeStatic
    def get_posted_by_full_name(self, request):
        return request.post.posted_by.get_full_name()

    # noinspection PyMethodMayBeStatic
    def get_requested_by_full_name(self, request):
        return request.requested_by.get_full_name()

    # noinspection PyMethodMayBeStatic
    def validate_requested_price(self, requested_price):
        if requested_price <= 0.0:
            raise serializers.ValidationError(MUST_BE_NON_NEGATIVE)
        return requested_price
