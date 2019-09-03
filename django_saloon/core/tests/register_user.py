"""Core test module."""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from core.utils import create_user_instance


class TestRegisterUser(APITestCase):
    """test case class for api login"""

    def setUp(self):
        """saving user for register test cases."""
        self.url = reverse('api_register')
        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'

        self.user = create_user_instance(
            self.username, self.email, self.password)

    def test_sucessful_register_saloon_user(self):
        """sucessful saloon user registration."""
        request_data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'saloon'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='abbas').exists())

    def test_sucessful_register_customer_user(self):
        """sucessful customer user registration."""
        request_data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'customer'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='rose').exists())

    def test_username_already_exsist_register_user(self):
        """failed user registration with already exsist username."""
        request_data = {
            'username': 'abbas',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'saloon'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_not_matched_register_user(self):
        """failed user registration with passwords not matched."""
        request_data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2',
            'user_type': 'saloon'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_type_not_specified_register_user(self):
        """failed user registration with user_type not specified."""
        request_data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_type_specified_register_user(self):
        """failed user registration with wrong user_type specified."""
        request_data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2',
            'type': 'teacher'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
