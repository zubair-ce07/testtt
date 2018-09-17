from datetime import timedelta
import jwt

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from datetime import datetime

from . import constants
from social_financer.settings import dev


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

def file_path_and_rename(instance, filename):
    return 'user_{}/{}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    DONOR = 'DN'
    CONSUMER = 'CN'
    ROLE_TYPES = (
        (DONOR, 'Donor'),
        (CONSUMER, 'Consumer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic_no = models.CharField(max_length=16)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    pair = models.ForeignKey('self', null=True, related_name='pairs', on_delete=models.SET_NULL, blank=True)
    categories = models.ManyToManyField(Category)
    role = models.CharField(max_length=2, choices=ROLE_TYPES)
    display_picture = models.ImageField(upload_to=file_path_and_rename, null=True)

    def __str__(self):
         return self.full_name() or self.username()

    def full_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def username(self):
        return self.user.username

    def is_paired(self):
        if self.role == UserProfile.DONOR:
            return False if self.pairs.count == 0 else True
        elif self.role == UserProfile.CONSUMER:
            return False if self.pair is None else True

    def get_pair(self):
        if self.role == UserProfile.DONOR:
            return self.pairs
        elif self.role == UserProfile.CONSUMER:
            return self.pair


class PairHistory(models.Model):
    """ A model that keeps record of breaking and making of users' pairs, used in admin
    """
    # This is true if the pair was made and false if the pair was broken.
    was_paired = models.BooleanField(default=True)
    date_logged = models.DateTimeField(default=datetime.now, blank = True)
    donor = models.ForeignKey(UserProfile, related_name='donor_pair_history', on_delete=models.CASCADE)
    consumer = models.ForeignKey(UserProfile, related_name='consumer_pair_history', on_delete=models.CASCADE)
    unpaired_by = models.CharField(max_length=2, choices=UserProfile.ROLE_TYPES)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
