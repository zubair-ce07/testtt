from url_crawler.models import CustomUser


class CustomAuthBackend(object):
    """
    Authentication backend for authenticated users with email and password
    """
    def authenticate(self, request, email, password):

        try:
            user = CustomUser.objects.get(email=email)

            if user.check_password(password):
                return user

        except CustomUser.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
