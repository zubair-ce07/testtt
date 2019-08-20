from django.contrib.auth.hashers import check_password
from taskmanager.models import CustomUser
from validate_email import validate_email


class EmailAndUsernameAuthBackend:
    def authenticate(self, request, **login_credentials):
        login_name = login_credentials['username']
        password = login_credentials['password']
        if login_name:
            is_valid = validate_email(login_name)
            try:
                if is_valid:
                    user = CustomUser.objects.get(email=login_name)
                else:
                    user = CustomUser.objects.get(username=login_name)
            except CustomUser.DoesNotExist:
                user = None
            if user and check_password(password, user.password):
                return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
