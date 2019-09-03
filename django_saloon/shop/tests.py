from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Reservation
from core.utils import (
    create_customer_user_instance, create_shop_user_instance,
    create_reservation_instance, create_time_slot_instance
)


class TestShopList(APITestCase):

    def setUp(self):
        """creating saloons shop list test case."""

        self.username = "rose"
        self.email = "rose@gmail.com"
        self.password = "rose"
        self.user = create_shop_user_instance(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

        create_shop_user_instance('ali', 'ali@gmail.com', 'ali')

    def shop_list(self):
        """Customer failed update test providing username that already exists."""

        url = reverse('api_shop_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
