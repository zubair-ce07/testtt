from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import UserProfile


class testCreateOwnerView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.name = 'random'
        self.password = 'm032245592'
        self.client.post('/add/owner/', {'username': self.name, 'password': self.password}, format='json')

    def test_is_owner_created(self):
        response = self.client.post('/auth/login/', {'username': self.name, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username=self.name)
        self.assertEqual('random', user.username)
        profile = UserProfile.objects.get(user=user)
        self.assertEqual('o', profile.user_type)


class TestCreateCustomerView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.name = 'random'
        self.password = 'm032245592'
        self.client.post('/add/customer/', {'username': self.name, 'password': self.password}, format='json')

    def test_is_owner_created(self):
        response = self.client.post('/auth/login/', {'username': self.name, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username=self.name)
        self.assertEqual('random', user.username)
        profile = UserProfile.objects.get(user=user)
        self.assertEqual('c', profile.user_type)


