from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    '''
    Extension of the User model to include employee data
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=32)
    supervisor = models.ForeignKey(User, related_name='supervisor', blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
