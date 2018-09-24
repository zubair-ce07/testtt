from django.urls import reverse

from custom_user.models import MyUser

DEFAULT_USERNAME = 'temporary'
DEFAULT_PASSWORD = 'temporary'
DEFAULT_EMAIL = 'temp@email.com'


def create_user(user_name=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD, first_name=None,
                last_name=None,
                email=None):
    """
    rhis method creates a user in DB
    :param user_name:
    :param passwd:
    :param first_name:
    :param last_name:
    :param email:
    :return:
    """
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
    """
    this function creates a dictionary for user attributes
    :param user_name:
    :param passwd:
    :param first_name:
    :param last_name:
    :param email:
    :return:
    """
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
    """
    this functions creates a dictionary for change password request
    :param old_passwd:
    :param new_passwd:
    :param repeat_passwd:
    :return:
    """
    request_data = dict()
    if old_passwd:
        request_data['old_password'] = old_passwd
    if new_passwd:
        request_data['new_password1'] = new_passwd
    if repeat_passwd:
        request_data['new_password2'] = repeat_passwd
    return request_data


def check_response(response, obj, check_list):
    """
    this function check the response with provided paramters
    :param response:
    :param obj:
    :param check_list:
    :return:
    """
    obj.assertEqual(response.status_code, 200)
    for checker in check_list:
        obj.assertContains(response, checker)


def create_and_login(obj):
    """
    this function create a user and login that user
    :param obj:
    :return:
    """
    create_user()
    obj.client.login(username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD)
