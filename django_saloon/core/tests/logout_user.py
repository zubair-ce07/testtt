"""Core test module."""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class LogoutTestCase(APITestCase):

    def setUp(self):
        """saving suser for logout test case."""
        self.url = reverse('api_logout')

        self.username = 'abbas'
        self.email = 'abbas@gmail.com'
        self.password = 'abbas'

        self.user = User.objects.create_user(
            self.username, self.email
        )
        self.user.set_password(self.password)
        self.user.save()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_logout_user(self):
        """
        Ensure we login.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=User.objects.get(
            username='abbas')).exists())
