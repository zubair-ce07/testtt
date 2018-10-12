"""
this module contains change password view test cases
"""
from django.test import TestCase
from django.urls import reverse
from . import utils


class CustomUserChangePasswordTest(TestCase):
    """
    it test user change password page
    """

    def test_unauthenticated_access(self):
        """
        it tests whether an unautorized person can access this page or not
        :return:
        """
        response = self.client.get(reverse('my_user:change_password'), follow=True)
        utils.check_response(response, self, ['Login'])

    def test_authenticated_access(self):
        """
        it tests whether an autorized person can access this page or not
        :return:
        """
        utils.create_and_login(self)
        response = self.client.get(reverse('my_user:change_password'))
        utils.check_response(response, self, ['Change Your Password'])

    # def test_correct_password_change(self):
    #     create_and_login(self)
    #     request_data = create_password_request(DEFAULT_PASSWORD, 'password', 'password')
    #     response = self.client.post(reverse('my_user:change_password'), request_data=request_data,
    #                                 follow=True)
    #     check_response(response, self, ['Please Login or Register First'])
