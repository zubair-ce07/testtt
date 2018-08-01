from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import serializers
# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url')
