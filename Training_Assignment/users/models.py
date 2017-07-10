import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from address.models import AddressField
from django.db.models import ImageField


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")], blank=True, max_length=15)
    country = CountryField()
    address = AddressField(related_name='+', blank=True, null=True)
    image = ImageField(upload_to='users/')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
