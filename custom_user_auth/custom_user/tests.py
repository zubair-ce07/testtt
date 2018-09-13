from django.test import TestCase
from django.urls import reverse

from .models import MyUser

DEFAULT_USERNAME = 'temporary'
DEFAULT_PASSWORD = 'temporary'
DEFAULT_EMAIL = 'temp@email.com'


def create_user(user_name=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD, first_name=None,
                last_name=None,
                email=None):
    my_user = MyUser.objects.create_user(username=user_name, password=passwd)
    if first_name:
        my_user.first_name = first_name
    if last_name:
        my_user.last_name = last_name
    if email:
        my_user.email = email
    my_user.save()


def create_request_data(user_name=None, passwd=None, first_name=None, last_name=None,
                        email=None):
    request_data = dict()
    if user_name:
        request_data['username'] = user_name
    if passwd:
        request_data['password'] = passwd
    if first_name:
        request_data['first_name'] = first_name
    if last_name:
        request_data['last_name'] = last_name
    if email:
        request_data['email'] = email
    return request_data


def create_password_request(old_passwd=None, new_passwd=None, repeat_passwd=None):
    request_data = dict()
    if old_passwd:
        request_data['old_password'] = old_passwd
    if new_passwd:
        request_data['new_password1'] = new_passwd
    if repeat_passwd:
        request_data['new_password2'] = repeat_passwd
    return request_data


def check_response(response, obj, check_list):
    obj.assertEqual(response.status_code, 200)
    for checker in check_list:
        obj.assertContains(response, checker)


def create_and_login(obj):
    create_user()
    obj.client.login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)


# class CustomUserIndexTests(TestCase):
#
#     def test_un_registered_user(self):
#         response = self.client.get(reverse('my_user:index'))
#         check_response(response, self, ['Please Login or Register First'])
#
#     def test_registered_user(self):
#         create_and_login(self)
#         response = self.client.get(reverse('my_user:index'))
#         check_response(response, self, ['Welcome user'])
#
#
# class CustomUserRegisterTest(TestCase):
#     # def test_registered_user(self):
#     #     create_user()
#     #     self.client.login(username='temporary', password='temporary')
#     #     response = self.client.get(reverse('my_user:index'))
#     #     self.assertEqual(response.status_code, 200)
#     #     # self.assertContains(response, 'Please Login or Register First')
#     #     self.assertContains(response, 'Welcome user')
#
#     def test_correct_register(self):
#         request_data = create_request_data(user_name=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD,
#                                            email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['Welcome user'])
#
#     def test_register_without_username(self):
#         request_data = create_request_data(passwd=DEFAULT_PASSWORD, email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['please enter a username'])
#
#     def test_register_without_password(self):
#         request_data = create_request_data(user_name=DEFAULT_USERNAME, email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['please enter your password'])
#
#     def test_register_without_any_field(self):
#         request_data = create_request_data()
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['please enter a username', 'please enter your password'])
#
#     def test_unique_username(self):
#         create_user()
#         request_data = create_request_data(user_name=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD,
#                                            email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['A user with that username already exists'])
#
#     def test_very_large_username(self):
#         request_data = create_request_data(user_name='hello' * 31, passwd=DEFAULT_PASSWORD,
#                                            email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:register'), request_data, follow=True)
#         check_response(response, self, ['username should be of maximum length of 150'])
#
#
# class CustomUserLoginTest(TestCase):
#
#     def test_correct_login(self):
#         create_user()
#         request_data = create_request_data(user_name=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD)
#         response = self.client.post(reverse('my_user:login'), request_data, follow=True)
#         check_response(response, self, ['Welcome user'])
#
#     def test_login_without_username(self):
#         request_data = create_request_data(passwd=DEFAULT_PASSWORD, email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:login'), request_data, follow=True)
#         check_response(response, self, ['please enter your username'])
#
#     def test_login_without_password(self):
#         request_data = create_request_data(user_name=DEFAULT_USERNAME, email=DEFAULT_EMAIL)
#         response = self.client.post(reverse('my_user:login'), request_data, follow=True)
#         check_response(response, self, ['please enter your password'])
#
#     def test_login_without_any_field(self):
#         request_data = create_request_data()
#         response = self.client.post(reverse('my_user:login'), request_data, follow=True)
#         check_response(response, self, ['please enter your username', 'please enter your password'])
#
#
# class CustomUserEditTest(TestCase):
#     def test_unauthenticated_access(self):
#         response = self.client.get(reverse('my_user:edit'), follow=True)
#         check_response(response, self, ['Login'])
#
#     def test_authenticated_access(self):
#         create_and_login(self)
#         response = self.client.get(reverse('my_user:edit'))
#         check_response(response, self, ['Edit Your Profile'])
#
#     def test_complete_edit_form(self):
#         create_and_login(self)
#         request_data = create_request_data(user_name="new_name", email="new@email.com",
#                                            first_name="test", last_name="user")
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#
#         checkers = [
#             'Welcome user "test user"',
#             'Your username is: new_name',
#             'Your email is: new@email.com'
#         ]
#         check_response(response, self, checkers)
#
#     def test_edit_form_without_firstname(self):
#         create_and_login(self)
#         request_data = create_request_data(user_name="new_name", email="new@email.com",
#                                            last_name="user")
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#
#         checkers = [
#             'Welcome user " user"',
#             'Your username is: new_name',
#             'Your email is: new@email.com'
#         ]
#         check_response(response, self, checkers)
#
#     def test_edit_form_without_laststname(self):
#         create_and_login(self)
#         request_data = create_request_data(user_name="new_name", email="new@email.com",
#                                            first_name="new")
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#
#         checkers = [
#             'Welcome user "new "',
#             'Your username is: new_name',
#             'Your email is: new@email.com'
#         ]
#         check_response(response, self, checkers)
#
#     def test_edit_form_without_email(self):
#         create_and_login(self)
#         request_data = create_request_data(user_name="new_name", first_name="test",
#                                            last_name="user")
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#
#         checkers = [
#             'Welcome user "test user"',
#             'Your username is: new_name',
#             'Your email is:'
#         ]
#         check_response(response, self, checkers)
#
#     def test_edit_form_without_username(self):
#         create_and_login(self)
#         request_data = create_request_data(email="new@email.com",
#                                            first_name="test", last_name="user")
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#         check_response(response, self, ['please enter a username'])
#
#     def test_very_large_username(self):
#         create_and_login(self)
#         request_data = create_request_data(user_name='hello' * 31)
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#         check_response(response, self, ['username should be of maximum length of 150'])
#
#     def test_very_large_firstname_and_lastname(self):
#         create_and_login(self)
#         request_data = create_request_data(first_name='hello' * 9, last_name='world' * 9)
#         response = self.client.post(reverse('my_user:edit'), request_data, follow=True)
#         check_response(response, self, ['firstname should be of maximum length of 40',
#                                         'lastname should be of maximum length of 40'])


class CustomUSerCHangePasswordTest(TestCase):
    def test_unauthenticated_access(self):
        response = self.client.get(reverse('my_user:change_password'), follow=True)
        check_response(response, self, ['Login'])

    def test_authenticated_access(self):
        create_and_login(self)
        response = self.client.get(reverse('my_user:change_password'))
        check_response(response, self, ['Change Your Password'])

    # def test_correct_password_change(self):
    #     create_and_login(self)
    #     request_data = create_password_request(DEFAULT_PASSWORD, 'password', 'password')
    #     print(request_data)
    #     response = self.client.post(reverse('my_user:change_password'), request_data=request_data)
    #     # check_response(response, self, ['Please Login or Register First'])
    #     print(response.content)