from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from taskmanager.models import CustomUser


class EmailAndUsernameAuthBackend:
    def authenticate(self, request, **login_credentials):
        login_name = login_credentials['username']
        password = login_credentials['password']
        if login_name:
            try:
                validate_email(login_name)
            except ValidationError:
                user = CustomUser.objects.get(username=login_name)
            else:
                user = CustomUser.objects.get(email=login_name)
            if user and check_password(password, user.password):
                return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
