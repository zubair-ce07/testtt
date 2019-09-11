"""Customer app serializer."""
from rest_framework import serializers
from customer.models import Customer
from core.serializers import UserUpdateSerializer


class CustomerUpdateSerializer(serializers.ModelSerializer):
    """Customer serializer for customer update."""

    user = UserUpdateSerializer()

    class Meta:
        """Customer Update Serializer meta class."""

        model = Customer
        fields = ('phone_no', 'user')

    def update(self, instance, validated_data):
        """Override Customer Update Serializer update method."""
        user = validated_data.pop('user')
        user_serializer = UserUpdateSerializer(
            data=user, instance=instance.user)
        user_serializer.is_valid()
        user_serializer.save()

        return super(CustomerUpdateSerializer, self).update(instance, validated_data)
