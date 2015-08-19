from web.users.models import User


class EmailAuthenticationBackend(object):

    # noinspection PyMethodMayBeStatic
    def authenticate(self, username=None, password=None):

        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
