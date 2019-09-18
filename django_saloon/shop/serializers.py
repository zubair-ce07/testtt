"""Shop app serializer module."""
from rest_framework import serializers

from core.serializers import UserUpdateSerializer
from shop.models import Saloon, TimeSlot, Reservation, Review
from customer.serializers import CustomerUpdateSerializer


class ShopSerializer(serializers.ModelSerializer):
    """Shop seriliazer."""

    rating = serializers.ReadOnlyField()

    class Meta:
        """Shop Serializer meta class."""

        model = Saloon
        fields = ('id', 'shop_name', 'phone_no', 'address', 'rating')


class SaloonUpdateSerializer(serializers.ModelSerializer):
    """Shop seriliazer for update."""

    user = UserUpdateSerializer()

    class Meta:
        """Saloon Update Serializer meta class."""

        model = Saloon
        fields = ('shop_name', 'phone_no', 'address', 'user')

    def update(self, instance, validated_data):
        """Saloon Update Serializer update override."""
        user = validated_data.pop('user')
        user_serializer = UserUpdateSerializer(
            data=user, instance=instance.user)
        user_serializer.is_valid()
        user_serializer.save()
        return super(SaloonUpdateSerializer, self).update(instance, validated_data)


class ListReviewSerializer(serializers.ModelSerializer):
    """Review list serializer."""

    class Meta:
        """Review list serializer meta class."""

        model = Review
        fields = ('comment', 'rating')


class SaloonSerializerForTimeSlotCustomer(serializers.ModelSerializer):
    """Shop seriliazer for update."""

    class Meta:
        """Saloon Update Serializer meta class."""

        model = Saloon
        fields = ('shop_name', 'phone_no', 'address', 'user')


class TimeSlotSerializerForCustomers(serializers.ModelSerializer):
    """Time slot serializer."""

    saloon = SaloonSerializerForTimeSlotCustomer(read_only=True)

    class Meta:
        """TimeSlotSerializer meta class."""

        model = TimeSlot
        fields = ('id', 'saloon', 'time', 'reservation')


class ReservationSerializer(serializers.ModelSerializer):
    """Reservation serializer."""

    review = serializers.ReadOnlyField()

    class Meta:
        """Reservation Serializer meta class."""

        model = Reservation
        fields = ('id', 'time_slot', 'customer', 'review')


class ReservationSerializerForCustomer(serializers.ModelSerializer):
    """Reservation serializer."""

    review = serializers.ReadOnlyField()
    time_slot = TimeSlotSerializerForCustomers()

    class Meta:
        """Reservation Serializer meta class."""

        model = Reservation
        fields = ('id', 'time_slot', 'customer', 'review')


class TimeSlotSerializer(serializers.ModelSerializer):
    """Time slot serializer."""

    reservation = ReservationSerializer()

    class Meta:
        """Time Slot Serializer meta class."""

        model = TimeSlot
        fields = ('saloon', 'time', 'reservation')


class ListReservationSerializer(serializers.ModelSerializer):
    """Reservation serializer."""

    review = ListReviewSerializer(read_only=True)
    customer = CustomerUpdateSerializer()
    time_slot = TimeSlotSerializer()

    class Meta:
        """Reservation Serializer meta class."""

        model = Reservation
        fields = ('id', 'time_slot', 'customer', 'review')


class ScheduleSerializer(serializers.Serializer):
    """Time slot schedule serializer."""

    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.IntegerField()
    number_of_slots = serializers.IntegerField()
    slot_duration = serializers.IntegerField()


class AddReviewSerializer(serializers.ModelSerializer):
    """Add review serializer."""

    class Meta:
        """Add review serializer meta class."""

        model = Review
        fields = '__all__'
