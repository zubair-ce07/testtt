from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    Profile Model
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    address = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    profile_photo = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def clean(self):
        if self.age and self.age < 0:
            raise ValidationError(_('Age must be positive'))

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Receiver when a new user entry is created a profile entry should be created.
    """
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save profile instances as well after `User` is updated.
    """
    instance.profile.save()
