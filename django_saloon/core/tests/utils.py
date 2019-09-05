"""core utils file."""
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from shop.models import Saloon, TimeSlot, Reservation
from customer.models import Customer


def create_user_instance(username, email, password):
    """create a user instance in db"""
    user = User.objects.create_user(
        username, email
    )
    user.set_password(password)
    user.save()
    return user


def create_customer_user_instance(username, email, password):
    """create a customer user instance in db"""
    user = create_user_instance(username, email, password)
    Customer.objects.create(user=user)
    return user


def create_shop_user_instance(username, email, password):
    """create a shop user instance in db"""
    user = create_user_instance(username, email, password)
    Saloon.objects.create(shop_name='rose saloon', user=user)
    return user


def create_time_slot_instance(saloon, time):
    """create a time_slot instance in db"""
    time_slot = TimeSlot(
        saloon=saloon, time=time)
    time_slot.save()
    return time_slot


def create_reservation_instance(time_slot, customer):
    """create a reservation instance in db"""
    reservation = Reservation(
        time_slot=time_slot, customer=customer)
    reservation.save()
    return reservation


class User_Mixin_Test_Case(APITestCase):
    """User test mixin class."""

    def setUp(self):
        """saving user for test case."""

        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'

        self.user = create_user_instance(
            self.username, self.email, self.password)
        self.user.set_password(self.password)
        self.user.save()


class Customer_Mixin_Test_Case(APITestCase):
    """User test mixin class."""

    def setUp(self):
        """saving user for test case."""

        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'

        self.user = create_customer_user_instance(
            self.username, self.email, self.password)


class Shop_Mixin_Test_Case(APITestCase):
    """User test mixin class."""

    def setUp(self):
        """creating saloons shop list test case."""

        self.username = "rose"
        self.email = "rose@gmail.com"
        self.password = "rose"
        self.user = create_shop_user_instance(
            self.username, self.email, self.password)

        self.customer_user = create_customer_user_instance(
            'ali', 'ali@gmail.com', 'ali')

        self.time_slot = create_time_slot_instance(
            self.user.saloon, datetime.now())

        self.reservation = create_reservation_instance(
            self.time_slot, self.customer_user.customer)
