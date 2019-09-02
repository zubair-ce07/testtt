"""customer test module."""
from datetime import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Reservation
from core.utils import (
    create_customer_user_instance, create_shop_user_instance,
    create_reservation_instance, create_time_slot_instance
)


class Test_Customer_Update(APITestCase):

    def setUp(self):
        """creating customer,saloon,timeslot and reservation for
        user reservation test case."""

        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"
        self.user = create_customer_user_instance(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

        create_customer_user_instance('ali', 'ali@gmail.com', 'ali')

    def test_sucessful_update_customer(self):
        """Customer sucessful update test."""

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

    def test_sucessful_only_username_update_customer(self):
        """Customer sucessful update test, updating username only."""

        url = reverse('api_customer_profile')
        data = {
            "user": {
                "username": "kami5"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            username='kami5'), self.user)

    def test_username_not_provided_update_customer(self):
        """Customer failed update test without username."""

        url = reverse('api_customer_profile')
        data = {
            "user": {
                "email": "abc@gmail.com"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exist_update_customer(self):
        """Customer failed update test providing username that already exists."""

        url = reverse('api_customer_profile')
        data = {
            "user": {
                "username": "ali"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_Customer_Reservation(APITestCase):

    def setUp(self):
        """creating customer,saloon,timeslot and reservation for
        user reservation test case."""

        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"
        self.user = create_customer_user_instance(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

        self.username = "rose"
        self.email = "rose@gmail.com"
        self.password = "rose"
        self.saloon_user = create_shop_user_instance(
            self.username, self.email, self.password)

        self.time_slot = create_time_slot_instance(
            self.saloon_user.saloon, datetime.now())

        self.reservation = create_reservation_instance(
            self.time_slot, self.user.customer)

    def test_customer_reservations_sucessful(self):
        """testing api customer list reservations."""
        url = reverse('api_customer_reservations')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.get(
            customer=self.user.customer), self.reservation)
