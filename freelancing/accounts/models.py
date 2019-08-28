from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)


def profile_images_path(instance, filename):
    """
        returns the path where the
        profile images should be stored
    """
    return "images/profile_images/{0}_{1}".format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=800, blank=True)
    country = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to=profile_images_path, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
