from rest_framework import serializers
from backend.users.models import UserInterest
from backend.users.serializers.user import UserSerializer
from backend.categories.serializers.category import CategorySerializer


class UserInterestSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = UserInterest
        fields = ('category', )
