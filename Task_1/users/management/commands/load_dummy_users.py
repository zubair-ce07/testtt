import csv

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from users.models import UserProfile


class Command(BaseCommand):
    def handle(self, **options):
        with open('users.csv', 'r') as csvfile:
            users_info = csv.DictReader(csvfile)
            users = []
            for user in users_info:
                users.append(UserProfile(
                    user=User.objects.create(username='{}.{}'.format(user['first_name'], user['last_name']),
                                             password=make_password(user['password']), first_name=user['first_name'],
                                             last_name=user['last_name'], email=user['email']),
                    phone_number=user['phone_number'], country=user['country'], address=user['address'],
                    image=user['image'], load_from_file=True))
            UserProfile.objects.bulk_create(users)

            # implementation using proxy class + post_save signal
            # for user in users_info:
            #     dummy_user = CustomUser(username='{}.{}'.format(user['first_name'], user['last_name']),
            #                             password=make_password(user['password']), email=user['email'],
            #                             first_name=user['first_name'], first_name=user['first_name'])
            #     users.append([dummy_user, {'phone_number': user['phone_number'], 'image': user['image'],
            #                                'country': user['country'], 'address': user['address']}])
            # CustomUser.objects.bulk_create(users)
