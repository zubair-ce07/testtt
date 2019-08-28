from rest_framework import serializers

from customer.models import Customer
from core.serializers import UserUpdateSerializer


class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email',
                  'username', 'user')
