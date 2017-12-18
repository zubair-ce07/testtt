from user_api.models import User
from django.core.validators import validate_email, ValidationError


class CustomAuthBackend(object):
    """
    Authentication backend for authenticating users with email and password
    """
    def _lookup_user(self, email_or_phone):
        """
        Tries to look up user on provided identifier that can
        be either email or phone number.

        Arguments:
            email_or_phone (str): to identify user from

        Returns:
            user (User): user associated with provided email or phone
        """
        try:
            validate_email(email_or_phone)
            user = User.objects.get(email=email_or_phone)
        except ValidationError:
            user = User.objects.get(phone=email_or_phone)

        return user

    def authenticate(self, request, email_or_phone, password):

        user = None

        try:
            un_auth_user = self._lookup_user(email_or_phone)

            if un_auth_user.check_password(password):
                user = un_auth_user

        except User.DoesNotExist:
            pass

        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None

        return user
