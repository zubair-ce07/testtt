"""Core test module."""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.tests.utils import User_Mixin_Test_Case


class LogoutTestCase(User_Mixin_Test_Case):
    """user logout test class."""

    def setUp(self):
        """saving user for login test case."""

        self.url = reverse('api_logout')
        super(LogoutTestCase, self).setUp()

    def test_sucessful_logout_user(self):
        """
        Ensure logout login.
        """
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=User.objects.get(
            username='abbas')).exists())

    def test_logout_user_no_user_logged_in(self):
        """
        log out without user login.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
