from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from datetime import datetime

from user import models

USER_MODEL = get_user_model()

class Command(BaseCommand):
    help = 'Insert dummy users into database'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        filename = options['filename']
        file = open(filename, 'r')
        file_list = file.read().split("end")
        for user in file_list:
            user_data = user.split()
            if user_data:
                try:
                    user = USER_MODEL.objects.create_user(
                        username=user_data[0],
                        first_name=user_data[1],
                        last_name=user_data[2],
                        email=user_data[3],
                        password=int(user_data[4]),
                        gender=user_data[5],
                    )
                    user_profile = models.UserProfile.objects.create(
                        country=user_data[6],
                        state=user_data[7],
                        city=user_data[8],
                        birthday=datetime.strptime(
                            user_data[9],
                            '%d-%m-%Y').date(),
                        user=user
                    )
                except Exception as e:
                    print("Database Exception: {0}".format(e.__cause__))
