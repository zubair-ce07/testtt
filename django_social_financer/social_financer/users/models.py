from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    cnic_no = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    role_types = (
        ('DN', 'Donor'),
        ('CN', 'Consumer'),
    )
    role = models.CharField(max_length=2, choices=role_types)
    pairId = models.ForeignKey('self', null=True, related_name='Profile', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
         return "{} {}".format(self.first_name, self.last_name)
