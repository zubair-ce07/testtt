"""Core test module."""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from core.tests.utils import User_Mixin_Test_Case


class TestRegisterUser(User_Mixin_Test_Case):
    """test case class for api login"""

    def setUp(self):
        """saving user for login test case."""

        self.url = reverse('api_register')

        super(TestRegisterUser, self).setUp()

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
        self.assertTrue(User.objects.filter(username='rose').exists())

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
