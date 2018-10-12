"""
this module contains change password view test cases
"""
from django.test import TestCase
from django.urls import reverse
from custom_user import strings
from . import utils


class CustomUserRegisterTest(TestCase):
    """
    it test user change password page
    """
    def test_logged_in_user(self):
        """
        it test logged in user
        :return:
        """
        utils.create_and_login(self)
        response = self.client.get(reverse('my_user:register'), follow=True)
        utils.check_response(response, self, ['Welcome user'])

    def test_correct_register(self):
        """
        it test correct register
        :return:
        """
        request_data = utils.create_request_data(user_name=utils.DEFAULT_USERNAME,
                                                 passwd=utils.DEFAULT_PASSWORD,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self, ['Welcome user'])

    def test_register_without_username(self):
        """
        test register without username
        :return:
        """
        request_data = utils.create_request_data(passwd=utils.DEFAULT_PASSWORD,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self, [strings.USERNAME_REQUIRED])

    def test_register_without_password(self):
        """
        test register without password
        :return:
        """
        request_data = utils.create_request_data(user_name=utils.DEFAULT_USERNAME,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self, [strings.PASSWORD_REQUIRED])

    def test_register_without_any_field(self):
        """
        it test register without any field
        :return:
        """
        request_data = utils.create_request_data()
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self,
                             [strings.USERNAME_REQUIRED, strings.PASSWORD_REQUIRED])

    def test_unique_username(self):
        """
        it test unique username
        :return:
        """
        utils.create_user()
        request_data = utils.create_request_data(user_name=utils.DEFAULT_USERNAME,
                                                 passwd=utils.DEFAULT_PASSWORD,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self, [strings.USERNAME_UNIQUE])

    def test_very_large_username(self):
        """
        it test very large username
        :return:
        """
        request_data = utils.create_request_data(user_name='hello' * 31,
                                                 passwd=utils.DEFAULT_PASSWORD,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:register'), request_data, follow=True)
        utils.check_response(response, self, [strings.USERNAME_MAX_LENGTH])
