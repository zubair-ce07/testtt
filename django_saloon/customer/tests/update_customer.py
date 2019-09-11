"""Customer test module."""

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from core.tests.utils import (Customer_Mixin_Test_Case,
                              create_customer_user_instance,
                              create_shop_user_instance)


class TestCustomerUpdate(Customer_Mixin_Test_Case):
    """Customer update test class."""

    def setUp(self):
        """Create customer,saloon,timeslot and reservation."""
        self.url = reverse('api_customer_profile')

        super(TestCustomerUpdate, self).setUp()
        self.client.force_authenticate(user=self.user)

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
        create_customer_user_instance('ali', 'ali@gmail.com', 'ali')
        request_data = {
            'user': {
                'username': 'ali'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shop_user_update_customer(self):
        """Customer failed update test updated by shop user."""
        user = create_shop_user_instance('ali', 'ali@gmail.com', 'ali')
        self.client.force_authenticate(user=user)
        request_data = {
            'user': {
                'username': 'ali'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_customer_without_logged_in(self):
        """Customer failed update test without being logged in."""
        self.client.logout()
        request_data = {
            'user': {
                'username': 'ali'
            }
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
