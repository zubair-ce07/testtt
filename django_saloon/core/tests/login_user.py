from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.utils import create_user_instance


class TestLoginUser(APITestCase):
    """test case class for api login"""

    def setUp(self):
        """saving user for login test case."""

        self.url = reverse('api_login')

        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'

        self.user = create_user_instance(
            self.username, self.email, self.password)

    def test_sucessful_login_user(self):
        """test case for sucessful user login."""
        request_data = {'username': 'abbas',
                        'password': 'abbas'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(user=User.objects.get(
            username='abbas')).key, response.data.get('token'))

    def test_wrong_username_login_user(self):
        """test case for failed user login with wrong username."""
        request_data = {'username': 'abbas121',
                        'password': 'abbas'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_password_login_user(self):
        """test case for user login with wrong password."""
        request_data = {'username': 'abbas',
                        'password': 'abbas123'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
