__author__ = 'abdul'
from datetime import datetime

from rest_framework import serializers

from accounts.models import UserProfile
from feedback.models import Feedback


class FeedbackModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Feedback
        exclude = ('given_to_user', 'given_by_user')

    def update(self, instance, validated_data):
        new_feedback = Feedback()
        new_feedback.given_to_user = instance
        user_id = self.context.get('by_user', -1)
        new_feedback.given_by_user = UserProfile.objects.get(id=user_id)
        new_feedback.star_rating = validated_data.get('star_rating', 0)
        new_feedback.comments = validated_data.get('comments', '')
        new_feedback.date_logged = datetime.now()
        new_feedback.save()
        return new_feedback
