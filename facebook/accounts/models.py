from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils.storage import OverwriteStorage


def upload_location(instance, filename):
    _, extension = filename.split('.')
    return 'profile_pictures/{}.{}'.format(instance.username, extension)


class FBUser(AbstractUser):
    profile_picture = models.ImageField(storage=OverwriteStorage(), upload_to=upload_location)

    def __str__(self):
        return self.username
