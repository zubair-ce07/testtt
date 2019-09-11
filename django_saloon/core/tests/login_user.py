"""Login user test case file."""
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User

from core.tests.utils import User_Mixin_Test_Case


class TestLoginUser(User_Mixin_Test_Case):
    """Test case class for api login."""

    def setUp(self):
        """Save user for login test case."""
        self.url = reverse('api_login')
        super(TestLoginUser, self).setUp()

    def test_sucessful_login_user(self):
        """Test case for sucessful user login."""
        request_data = {'username': 'abbas',
                        'password': 'abbas'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(user=User.objects.get(
            username='abbas')).key, response.data.get('token'))

    def test_wrong_username_login_user(self):
        """Test case for failed user login with wrong username."""
        request_data = {'username': 'abbas121',
                        'password': 'abbas'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_password_login_user(self):
        """Test case for user login with wrong password."""
        request_data = {'username': 'abbas',
                        'password': 'abbas123'}
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
