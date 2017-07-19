import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from registration.models import CustomUser


class Command(BaseCommand):
    def handle(self, **options):
        with open('dummy.csv', 'r') as csvfile:
            users = csv.DictReader(csvfile)
            users_list = []
            for user in users:
                dummy_user = CustomUser(username='{}.{}'.format(user['first_name'], user['last_name']),
                                        password=make_password(user['password']), email=user['email'],
                                        first_name=user['first_name'], last_name=user['last_name'])
                users_list.append([dummy_user, {'phone_number': user['phone_number'], 'image': user['image'],
                                                'country': user['country'], 'address': user['address']}])
            CustomUser.objects.bulk_create(users_list)
