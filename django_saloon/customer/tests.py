"""customer test module."""
from datetime import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from customer.models import Customer
from shop.models import Reservation, TimeSlot, Saloon


class TestCustomer(APITestCase):

    def setUp(self):
        """creating customer,saloon,timeslot and reservation for
        user reservation test case."""

        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"
        self.user = User.objects.create_user(
            self.username, self.email
        )
        self.user.set_password(self.password)
        self.user.save()
        Customer.objects.create(user=self.user)

        self.client.force_authenticate(user=self.user)

        self.username = "rose"
        self.email = "rose@gmail.com"
        self.password = "rose"
        self.saloon_user = User.objects.create_user(
            self.username, self.email
        )
        self.saloon_user.set_password(self.password)
        self.saloon_user.save()
        Saloon.objects.create(user=self.saloon_user)

        self.time_slot = TimeSlot(
            saloon=self.saloon_user.saloon, time=datetime.now())
        self.time_slot.save()

        self.reservation = Reservation(
            time_slot=self.time_slot, customer=self.user.customer)
        self.reservation.save()

    def test_update_customer(self):
        """Customer update test."""

        url = reverse('api_customer_profile')
        data = {
            "user": {
                "username": "kami5",
                "email": "abc@gmail.com",
                "firstname": "abbas"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            username='kami5'), self.user)

    def test_customer_reservations(self):
        """testing api customer list reservations."""
        url = reverse('api_customer_reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.get(
            customer=self.user.customer), self.reservation)
