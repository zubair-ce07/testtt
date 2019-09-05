"""shop app serializer module."""
from rest_framework import serializers

from core.serializers import UserUpdateSerializer
from shop.models import Saloon, TimeSlot, Reservation, Review


class ShopSerializer(serializers.ModelSerializer):
    """shop seriliazer"""
    rating = serializers.ReadOnlyField()

    class Meta:
        """ShopSerializer meta class"""
        model = Saloon
        fields = ('id', 'shop_name', 'phone_no', 'address', 'rating')


class SaloonUpdateSerializer(serializers.ModelSerializer):
    """shop seriliazer for update"""
    user = UserUpdateSerializer()

    class Meta:
        """SaloonUpdateSerializer meta class"""
        model = Saloon
        fields = ('shop_name', 'phone_no', 'address', 'user')

    def update(self, instance, validated_data):
        """SaloonUpdateSerializer update override"""
        user = validated_data.pop('user')
        user_serializer = UserUpdateSerializer(
            data=user, instance=instance.user)
        user_serializer.is_valid()
        user_serializer.save()
        return super(SaloonUpdateSerializer, self).update(instance, validated_data)


class ListReviewSerializer(serializers.ModelSerializer):
    """review list serializer"""
    class Meta:
        """"review list serializer meta class"""
        model = Review
        fields = ('comment', 'rating')


class ListReservationSerializer(serializers.ModelSerializer):
    """reservation serializer"""

    review = ListReviewSerializer(read_only=True)

    class Meta:
        """ReservationSerializer meta class"""
        model = Reservation
        fields = ('time_slot', 'customer', 'review')


class ReservationSerializer(serializers.ModelSerializer):
    """reservation serializer"""
    review = serializers.ReadOnlyField()

    class Meta:
        """ReservationSerializer meta class"""
        model = Reservation
        fields = ('time_slot', 'customer', 'review')


class TimeSlotSerializer(serializers.ModelSerializer):
    """time slot serializer"""
    reservation = ReservationSerializer()

    class Meta:
        """TimeSlotSerializer meta class"""
        model = TimeSlot
        fields = ('saloon', 'time', 'reservation')


class TimeSlotSerializerForCustomers(serializers.ModelSerializer):
    """time slot serializer"""
    class Meta:
        """TimeSlotSerializer meta class"""
        model = TimeSlot
        fields = ('saloon', 'time', 'reservation')


class ScheduleSerializer(serializers.Serializer):
    """time slot schedule serializer"""
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.IntegerField()
    number_of_slots = serializers.IntegerField()
    slot_duration = serializers.IntegerField()


class AddReviewSerializer(serializers.ModelSerializer):
    """add review serializer"""
    class Meta:
        """add review serializer meta class"""
        model = Review
        fields = '__all__'
