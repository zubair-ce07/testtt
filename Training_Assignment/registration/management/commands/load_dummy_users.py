import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from registration.models import CustomUser


class Command(BaseCommand):
    def handle(self, **options):
        user_list = []
        with open('dummy.csv', 'r') as csvfile:
            users = csv.DictReader(csvfile)
            for user in users:
                user_list.append(user)
                username = user['username']
                password1 = user['password1']
                password2 = user['password2']
                phone_number = user['phone_number']
                country_name = user['country']
                address = user['address']
                image = user['image']
                #  UserProfile.objects.get_or_create(phone_number='+9874561231')
                # CustomUser.objects.create_user(username, password=password1)
                password1 = make_password(password1)
                u = CustomUser(username=username, password=password1)
                # up = UserProfile(
                # user=u, phone_number=phone_number, test='abdg')
                u.save(phone_number=phone_number,
                       country_name=country_name, address=address, image=image)
            # users = []
        csvfile.close()
        # print('bla')
        # print(user_list)
