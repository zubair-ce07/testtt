from user_api.models import User


class CustomAuthBackend(object):
    """
    Authentication backend for authenticating users with email and password
    """
    def authenticate(self, request, email, password):

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
