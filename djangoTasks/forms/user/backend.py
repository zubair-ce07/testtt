from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailAuthenticationBackend(ModelBackend):
    """
    custom backend model for authentication on the basis of username/email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        authenticate users on the basis of username/email & password
        :param request: HttpRequest object
        :param username: username field's value of myuser model
        :param password: password for authentication
        :returns: user model's object if user is authenticated
        :raises: DoesNotExit: raise an exception if user not found
        """
        try:
            user = get_user_model().objects.get(username=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            pass
        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            pass
        return None


class WithoutPasswordAuthenticationBackend(ModelBackend):
    """
            custom backend model for authentication without password
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        authenticate users on the basis of just username or email
        :param request: HttpRequest object
        :param username: username field's value of myuser model
        :param password: password for authentication
        :returns: user model's object if user is authenticated
        :raises: DoesNotExit: raise an exception if user not found
        """
        try:
            if not password:
                user = get_user_model().objects.get(username=username)
                return user
        except get_user_model().DoesNotExist:
                return None
