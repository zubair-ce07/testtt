import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from django_countries.fields import Country
# from django_countries.data import COUNTRIES

from registration.models import CustomUser, UserProfile


class Command(BaseCommand):
    def handle(self, **options):
        # COUNTRY_NAMES = dict([[name, code] for code, name in COUNTRIES.items()])
        with open('dummy.csv', 'r') as csvfile:
            users_info = csv.DictReader(csvfile)
            users = []

            for user in users_info:
                u = UserProfile(
                    user=User.objects.create(username='{}.{}'.format(user['first_name'], user['last_name']),
                                             password=make_password(user['password']), first_name=user['first_name'],
                                             last_name=user['last_name']), phone_number=user['phone_number'],
                    country=user['country'], address=user['address'], image=user['image'])
                u.save(load_from_text=True)

                # for user in users_info:
                #     dummy_user = CustomUser(username='{}.{}'.format(user['first_name'], user['last_name']),
                #                             password=make_password(user['password']), email=user['email'],
                #                             first_name=user['first_name'], first_name=user['first_name'])
                #     users.append([dummy_user, {'phone_number': user['phone_number'], 'image': user['image'],
                #                                'country': user['country'], 'address': user['address']}])
                # CustomUser.objects.bulk_create(users)
