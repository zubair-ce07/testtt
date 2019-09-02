"""Core test module."""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from core.utils import create_user_instance


class Test_Login_User(APITestCase):
    """test case class for api login"""

    def setUp(self):
        """saving user for login test case."""
        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"

        self.user = create_user_instance(
            self.username, self.email, self.password)

    def test_sucessful_login_user(self):
        """test case for sucessful user login."""
        url = reverse('api_login')
        data = {'username': 'abbas',
                'password': 'abbas'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, 'abbas')

    def test_wrong_username_login_user(self):
        """test case for failed user login with wrong username."""
        url = reverse('api_login')
        data = {'username': 'abbas121',
                'password': 'abbas'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_password_login_user(self):
        """test case for user login with wrong password."""
        url = reverse('api_login')
        data = {'username': 'abbas',
                'password': 'abbas123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_Register_User(APITestCase):
    """test case class for api login"""

    def setUp(self):
        """saving user for register test cases."""
        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"

        self.user = create_user_instance(
            self.username, self.email, self.password)

    def test_sucessful_register_saloon_user(self):
        """sucessful saloon user registration."""
        url = reverse('api_register')
        data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'saloon'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_sucessful_register_customer_user(self):
        """sucessful customer user registration."""
        url = reverse('api_register')
        data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_username_already_exsist_register_user(self):
        """failed user registration with already exsist username."""
        url = reverse('api_register')
        data = {
            'username': 'abbas',
            'password1': 'rose',
            'password2': 'rose',
            'user_type': 'saloon'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_password_not_matched_register_user(self):
        """failed user registration with passwords not matched."""
        url = reverse('api_register')
        data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2',
            'user_type': 'saloon'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_type_not_specified_register_user(self):
        """failed user registration with user_type not specified."""
        url = reverse('api_register')
        data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_wrong_type_specified_register_user(self):
        """failed user registration with wrong user_type specified."""
        url = reverse('api_register')
        data = {
            'username': 'rose',
            'password1': 'rose',
            'password2': 'rose2',
            'type': 'teacher'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class LogoutAPIViewTestCase(APITestCase):

    def setUp(self):
        """saving suser for logout test case."""
        self.username = "abbas"
        self.email = "abbas@gmail.com"
        self.password = "abbas"

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
        url = reverse('api_logout')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
