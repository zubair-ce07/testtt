"""customer test module."""

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from core.utils import create_customer_user_instance


class TestCustomerUpdate(APITestCase):

    def setUp(self):
        """creating customer,saloon,timeslot and reservation for
        user reservation test case."""
        self.url = reverse('api_customer_profile')
        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'
        self.user = create_customer_user_instance(
            self.username, self.email, self.password)
        self.client.force_authenticate(user=self.user)

        create_customer_user_instance('ali', 'ali@gmail.com', 'ali')

    def test_sucessful_update_customer(self):
        """Customer sucessful update test."""
        request_data = {
            'user': {
                'username': 'kami5',
                'email': 'abc@gmail.com',
                'firstname': 'abbas'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            username='kami5'), self.user)

    def test_sucessful_only_username_update_customer(self):
        """Customer sucessful update test, updating username only."""
        request_data = {
            'user': {
                'username': 'kami5'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(
            username='kami5'), self.user)

    def test_username_not_provided_update_customer(self):
        """Customer failed update test without username."""
        request_data = {
            'user': {
                'email': 'abc@gmail.com'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exist_update_customer(self):
        """Customer failed update test providing username that already exists."""
        request_data = {
            'user': {
                'username': 'ali'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
