from users.models import User


class CustomAuthBackend(object):
    """
    Authentication backend for authenticating users with email and password
    """
    def authenticate(self, request, email, password):

        user = None

        try:
            un_auth_user = User.objects.get(email=email)

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
