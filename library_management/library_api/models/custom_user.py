from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """Creating this class to add extra fields if required in future"""
    def __str__(self):
        """String for representing the Model object."""
        return self.username

    def inspect(self):
        return self.__dict__


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
