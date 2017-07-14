import csv
from memoapp.models import User
from django.contrib.auth.hashers import make_password, check_password


class FileBackend(object):
    def authenticate(self,request, email=None, password=None):
        with open('users.txt', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                if email == line[1] and check_password(password, line[2]):
                    user = User(id=line[0], email=email, password=password)
                    # print(user.is_authenticated())
                    return user
            return None

    def get_user(self, user_id):
        with open('users.txt', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                if str(user_id) == line[0]:
                    user = User(id=line[0], email=line[1], password=line[2])
                    return user
            return None

