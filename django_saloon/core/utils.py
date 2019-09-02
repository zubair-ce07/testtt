from django.contrib.auth.models import User

from shop.models import Saloon, TimeSlot, Reservation
from customer.models import Customer


def create_user_instance(username, email, password):
    user = User.objects.create_user(
        username, email
    )
    user.set_password(password)
    user.save()
    return user


def create_customer_user_instance(username, email, password):
    user = create_user_instance(username, email, password)
    Customer.objects.create(user=user)
    return user


def create_shop_user_instance(username, email, password):
    user = create_user_instance(username, email, password)
    Saloon.objects.create(user=user)
    return user


def create_time_slot_instance(saloon, time):
    time_slot = TimeSlot(
        saloon=saloon, time=time)
    time_slot.save()
    return time_slot


def create_reservation_instance(time_slot, customer):
    reservation = Reservation(
        time_slot=time_slot, customer=customer)
    reservation.save()
    return reservation
