from ehub.models import User
from django.contrib.auth.hashers import make_password

class MyBackEnd():
    @staticmethod
    def authenticate(username=None, password=None):
        try:
            hashed_password = make_password(password)
            user = User.objects.get(email=username, password=hashed_password)
            return user
        except User.DoesNotExist:
            return None
