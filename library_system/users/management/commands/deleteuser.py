"""Module for admin command for deleting user."""

from django.core.management.base import BaseCommand
from users.models import UserProfile as User

class Command(BaseCommand):
    """Class for deleting user from console."""

    help = 'Delete users'

    def add_arguments(self, parser):
        """Class for getting arguments from console."""
        parser.add_argument('user_id', nargs='+', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        """Class for handling arguments from console."""
        users_ids = kwargs['user_id']

        for user_id in users_ids:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                self.stdout.write('User "%s (%s)" deleted with success!' % (user.username, user_id))
            except User.DoesNotExist:
                self.stdout.write('User with id "%s" does not exist.' % user_id)
