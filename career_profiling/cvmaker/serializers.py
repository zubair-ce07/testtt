from rest_framework import serializers
from .models import (
    User,
    Profile,
    Experience,
    Education,
    Skill
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'first_name', 'last_name')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class EducationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
