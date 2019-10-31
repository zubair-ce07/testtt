"""Module for admin command for creating user."""

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from users.models import UserProfile as User


class Command(BaseCommand):
    """Class for creating user from console."""

    help = 'creates new user'

    def add_arguments(self, parser):
        """Class for getting arguments from console."""
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        """Class for handling arguments from console."""
        try:
            usernames = kwargs['username']
            passwords = kwargs['password']
            for name in usernames:
                username = name
            for user_password in passwords:
                password = user_password
            User.objects.create_user(username=username, password=password)
            User.objects.get(username=username).save()
            self.stdout.write(self.style.SUCCESS('Successfully created user "%s"' % username))
        except IntegrityError:
            raise CommandError('"%s" username already exists in the database.' % username)
