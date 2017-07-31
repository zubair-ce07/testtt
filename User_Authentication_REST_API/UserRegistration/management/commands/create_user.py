import getpass

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from UserRegistration.models import User


class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = options['count']
        users = []
        for user_number in range(count):
            user = User(first_name='User%dFirstName' % user_number, last_name='User%dLastName' % user_number,
                        username='user%d' % user_number, email='user%d@gmail.com' % user_number,
                        password=make_password("asdasdasd"), city='Lhr', is_active=True)
            users.append(user)
        User.objects.bulk_create(users)
        # from pip._vendor.distlib.compat import raw_input
        # email = self.check_email_contains(raw_input("Email: "), "@.")
        # password = getpass.getpass('Password: ')
        # username = raw_input('Username: ')
        # city = raw_input('City: ')
        # first_name = raw_input('First Name: ')
        # last_name = raw_input('Last Name: ')
        # CustomUser.objects.create_user(email=email, password=password, username=username,
        #                                city=city, first_name=first_name, last_name=last_name)

    def check_email_contains(self, email_address, characters, min_length=10):
        while True:
            from pip._vendor.distlib.compat import raw_input
            for character in characters:
                if character not in email_address:
                    email_address = raw_input(
                        "Enter valid email address: ")
                    continue
            if len(email_address) <= min_length:
                email_address = raw_input("Your email address is too short\nPlease write your email address again: ")
                continue
            return email_address
