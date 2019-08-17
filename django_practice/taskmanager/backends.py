from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from taskmanager.models import CustomUser


class EmailAndUsernameAuthBackend:
    def authenticate(self, request, username=None, password=None):
        if username:
            try:
                validate_email(username)
            except ValidationError:
                user = CustomUser.objects.get(username=username)
            else:
                user = CustomUser.objects.get(username=CustomUser.objects.get(email=username))
            if user and check_password(password, user.password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
