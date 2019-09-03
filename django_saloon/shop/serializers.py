"""shop app serializer module."""
from rest_framework import serializers
from django.contrib.auth.models import User

from core.serializers import UserUpdateSerializer
from shop.models import Saloon, TimeSlot, Reservation


class ShopSerializer(serializers.ModelSerializer):
    """shop seriliazer"""
    class Meta:
        """ShopSerializer meta class"""
        model = Saloon
        fields = ('id', 'shop_name', 'phone_no', 'address')


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
        User.objects.update_or_create(id=instance.user.id, defaults=user)

        return super(SaloonUpdateSerializer, self).update(instance, validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    """reservation serializer"""
    class Meta:
        """ReservationSerializer meta class"""
        model = Reservation
        fields = ('time_slot', 'customer')


class TimeSlotSerializer(serializers.ModelSerializer):
    """time slot serializer"""
    reservation = ReservationSerializer()

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
