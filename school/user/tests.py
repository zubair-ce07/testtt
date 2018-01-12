from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from user.fixtures.user_fixture import UserFixture


class UserTestCase(TestCase):
    
    def setUp(self):
        
        self.user_fixture = UserFixture()
        self.client = APIClient()
        

    def test_registration(self):
        
        user_data = self.user_fixture.get_user_data()
        response = self.client.post(
            reverse('rest_register'),
            user_data,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
