from rest_framework import serializers
from web.posts.models import Request


class ProcessRequestSerializer(serializers.ModelSerializer):

    user_id = serializers.PrimaryKeyRelatedField(source='requested_by', read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'user_id', 'post_id', 'status')

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        if status == Request.StatusChoices.ACCEPTED:
            instance.post.is_sold = True
            instance.post.save()
            instance.post.requests.filter(status=Request.StatusChoices.PENDING).\
                exclude(pk=instance.id).\
                update(status=Request.StatusChoices.REJECTED)
            instance.status = status
        else:
            instance.status = status
        instance.save()
        return instance

