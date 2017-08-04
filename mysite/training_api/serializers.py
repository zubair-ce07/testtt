from django.contrib.auth.models import User

from rest_framework import serializers

from training.models import (
    Trainee, Trainer, UserProfile,
    Assignment, Technology
)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['name', 'picture']


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology
        fields = ['id', 'name', 'description']


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'completion_status',
                  'technology_used']


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(serializers.ModelSerializer,
                                         read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_profile', 'username', 'password', 'first_name',
                  'last_name']


class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer(serializers.ModelSerializer)

    class Meta:
        model = Trainer
        fields = ['id', 'user']


class TraineeSerializer(serializers.ModelSerializer):
    user = UserSerializer(serializers.ModelSerializer)

    class Meta:
        model = Trainee
        fields = ['id', 'user', 'trainer']
