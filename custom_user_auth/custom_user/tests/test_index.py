"""
this module contains index view test cases
"""

from django.test import TestCase
from django.urls import reverse
from . import utils


class CustomUserIndexTests(TestCase):
    """
    it test user change password page
    """

    def test_un_registered_user(self):
        """
        it test unregistered user
        :return:
        """
        response = self.client.get(reverse('my_user:index'))
        utils.check_response(response, self, ['Please Login or Register First'])

    def test_registered_user(self):
        """
        it test registered user
        :return:
        """
        utils.create_and_login(self)
        response = self.client.get(reverse('my_user:index'))
        utils.check_response(response, self, ['Welcome user'])
