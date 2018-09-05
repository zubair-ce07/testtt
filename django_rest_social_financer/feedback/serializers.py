__author__ = 'abdul'
from rest_framework import serializers

from .models import Feedback
from accounts.models import UserProfile

class FeedbackModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        new_feedback = Feedback()
        new_feedback.given_to_user = self.instance
        user_id = self.context.get('by_user', -1)
        new_feedback.given_by_user = UserProfile.objects.get(id=user_id)
        new_feedback.star_rating = validated_data.get('star_rating', 0)
        new_feedback.comments = validated_data.get('comments', '')
        new_feedback.save()
        return new_feedback
