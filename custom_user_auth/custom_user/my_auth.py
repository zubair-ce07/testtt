"""
this module contains a custom authentication
"""
from .models import MyUser


class MyAuthBackend(object):
    """
    custom auhtentication class
    """

    def authenticate(self, request, username=None, password=None):
        """
        this method authenticate a user againsta username and password
        :param request:
        :param username:
        :param password:
        :return:
        """
        try:
            user = MyUser.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except MyUser.DoesNotExist:
            # raise ValidationError("Please provide  valid username and password")
            return None

    def get_user(self, user_id):
        """
        this method return a user against provided user_id
        :param user_id:
        :return:
        """
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None
