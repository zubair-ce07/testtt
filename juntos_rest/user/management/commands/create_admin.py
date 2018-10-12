from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    """
    Add admin user into the db
    """
    help = "Create Admin Accounts."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Handles command"""
        group, created = Group.objects.get_or_create(name='Admin')
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                first_name='Site',
                last_name='Admin',
                password='1234'
            )
            user.groups.set([group])
            user.is_superuser = True
            user.save()
        except IntegrityError:
            self.stdout.write(self.style.WARNING(
                'A superuser with the same username="admin" is already there -- [SKIPPING]'
            ))
        self.stdout.write(
            self.style.SUCCESS("Super user has been setup successfully. Username: admin, password: 1234")
        )
