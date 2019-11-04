from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
