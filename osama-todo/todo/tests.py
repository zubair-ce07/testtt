from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from .models import TodoItem
from .views import UserViewSet


class TodoItemTestCase(TestCase):
    """
    Test suite for TodoItem model
    """

    def setUp(self):
        self.user1 = User.objects.create(username='user1')

    def test_user_creation_post_request(self):
        """
        Tests a single user creationg
        """
        self.assertEqual('user1', self.user1.username)
