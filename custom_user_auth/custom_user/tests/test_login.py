"""
this module contains change password view test cases
"""
from django.test import TestCase
from django.urls import reverse
from custom_user import strings
from . import utils


class CustomUserLoginTest(TestCase):
    """
        it test user login page
    """

    def test_logged_in_user(self):
        """
        it test logged in user
        :return:
        """
        utils.create_and_login(self)
        response = self.client.get(reverse('my_user:login'), follow=True)
        utils.check_response(response, self, ['Welcome user'])

    def test_correct_login(self):
        """
        it test correct login
        :return:
        """
        utils.create_user()
        request_data = utils.create_request_data(user_name=utils.DEFAULT_USERNAME,
                                                 passwd=utils.DEFAULT_PASSWORD)
        response = self.client.post(reverse('my_user:login'), request_data, follow=True)
        utils.check_response(response, self, ['Welcome user'])

    def test_login_without_username(self):
        """
        it test login without username
        :return:
        """
        request_data = utils.create_request_data(passwd=utils.DEFAULT_PASSWORD,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:login'), request_data, follow=True)
        utils.check_response(response, self, [strings.USER_USERNAME_REQUIRED])

    def test_login_without_password(self):
        """
        test login without password
        :return:
        """
        request_data = utils.create_request_data(user_name=utils.DEFAULT_USERNAME,
                                                 email=utils.DEFAULT_EMAIL)
        response = self.client.post(reverse('my_user:login'), request_data, follow=True)
        utils.check_response(response, self, [strings.USER_PASSWORD_REQUIRED])

    def test_login_without_any_field(self):
        """
            test login without any field
        :return:
        """
        request_data = utils.create_request_data()
        response = self.client.post(reverse('my_user:login'), request_data, follow=True)
        utils.check_response(response, self,
                             [strings.USER_USERNAME_REQUIRED, strings.USER_PASSWORD_REQUIRED])
