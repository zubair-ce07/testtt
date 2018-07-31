from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import serializers
# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'url', 'username', 'email', 'is_staff')
