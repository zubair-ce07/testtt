from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Saloon

contact_number_validator = RegexValidator(regex=r'^\+?\d{9,15}$',
                                          message='Phone number must be entered in the format: +999999999'
                                                  '. Up to 15 digits allowed.')

USER_TYPES = (
    ('o', 'Owner'),
    ('c', 'Customer'),
    ('e', 'Employee'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True, default='images/None/No-image.png')
    contact_number = models.CharField(validators=[contact_number_validator], max_length=16, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPES,
        blank=True,
        default='c',
        help_text='User Role',
    )

    saloon = models.ForeignKey(Saloon, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}\'s profile'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
