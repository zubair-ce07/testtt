from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_num = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, blank=True)
    created_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.owner.username
