from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic_no = models.CharField(max_length=16)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    role_types = (
        ('DN', 'Donor'),
        ('CN', 'Consumer'),
    )
    role = models.CharField(max_length=2, choices=role_types)
    pairId = models.ForeignKey('self', null=True, related_name='Profile', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
         return self.get_full_name() if self.get_full_name() else self.get_username()

    def get_full_name(self):
        return "{}{}".format(self.user.first_name, self.user.last_name)

    def get_username(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()