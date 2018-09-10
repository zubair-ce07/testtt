from .models import MyUser
from django.core.exceptions import ValidationError

class MyAuthBackend(object):

    def authenticate(self, request, username=None, password=None):
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
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None