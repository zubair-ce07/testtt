"""
this module contains edit profile view test cases
"""
from django.test import TestCase
from django.urls import reverse
from custom_user import strings
from . import utils



class CustomUserEditTest(TestCase):
    """
     it test user's profile edit fpage
    """

    def test_unauthenticated_access(self):
        """
        it tests whether an unautorized person can access this page or not
        :return:
        """
        response = self.client.get(reverse('my_user:edit'), follow=True)
        utils.check_response(response, self, ['Login'])

    def test_authenticated_access(self):
        """
            it tests whether an unautorized person can access this page or not
            :return:
        """
        utils.create_and_login(self)
        response = self.client.get(reverse('my_user:edit'))
        utils.check_response(response, self, ['Edit Your Profile'])

    def test_complete_edit_form(self):
        """
        test edit form with all credentials
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(user_name="new_name", email="new@email.com",
                                                 first_name="test", last_name="user")
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)

        checkers = [
            'Welcome user "test user"',
            'Your username is: new_name',
            'Your email is: new@email.com'
        ]
        utils.check_response(response, self, checkers)

    def test_edit_form_without_firstname(self):
        """
        test edit form without firstname
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(user_name="new_name", email="new@email.com",
                                                 last_name="user")
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)

        checkers = [
            'Welcome user " user"',
            'Your username is: new_name',
            'Your email is: new@email.com'
        ]
        utils.check_response(response, self, checkers)

    def test_edit_form_without_laststname(self):
        """
        test edit form without laststname
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(user_name="new_name", email="new@email.com",
                                                 first_name="new")
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)

        checkers = [
            'Welcome user "new "',
            'Your username is: new_name',
            'Your email is: new@email.com'
        ]
        utils.check_response(response, self, checkers)

    def test_edit_form_without_email(self):
        """
        test edit form without email
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(user_name="new_name", first_name="test",
                                                 last_name="user")
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)

        checkers = [
            'Welcome user "test user"',
            'Your username is: new_name',
            'Your email is:'
        ]
        utils.check_response(response, self, checkers)

    def test_edit_form_without_username(self):
        """
        test edit form without username
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(email="new@email.com",
                                                 first_name="test", last_name="user")
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
        utils.check_response(response, self, [strings.USERNAME_REQUIRED])

    def test_very_large_username(self):
        """
        test very large username
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(user_name='hello' * 31)
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
        utils.check_response(response, self, [strings.USERNAME_MAX_LENGTH])

    def test_very_large_firstname_and_lastname(self):
        """
        test very large firstname and lastname
        :return:
        """
        utils.create_and_login(self)
        request_data = utils.create_request_data(first_name='hello' * 9, last_name='world' * 9)
        response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
        utils.check_response(response, self,
                             [strings.FIRSTNAME_MAX_LENGTH, strings.LASTNAME_MAX_LENGTH])
