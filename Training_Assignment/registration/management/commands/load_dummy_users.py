import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from registration.models import CustomUser


class Command(BaseCommand):
    def handle(self, **options):
        with open('dummy.csv', 'r') as csvfile:
            users = csv.DictReader(csvfile)
            for user in users:
                password = user['password']
                phone_number = user['phone_number']
                country_name = user['country']
                address = user['address']
                image = user['image']
                first_name = user['first_name']
                last_name = user['last_name']
                email = user['email']
                username = first_name + '.' + last_name
                password = make_password(password)
                dummy_user = CustomUser(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=email)
                dummy_user.save(phone_number=phone_number,
                                country_name=country_name, address=address, image=image, first_name=first_name)
