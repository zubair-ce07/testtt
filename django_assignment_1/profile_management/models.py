from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_photo = models.ImageField(upload_to='images',
                                      default="default.png")

    def __str__(self):
        return self.username

    def image_url(self):
        """This method check the url of the image"""
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url

        return None
