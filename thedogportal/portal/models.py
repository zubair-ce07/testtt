from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def update_filename(instance, fname):
    path = "uploads/"
    time_now = str(datetime.now()).split('.')[0]
    owner = str(instance.owner_id)

    formatting = owner + '_' + time_now + '_' + fname

    return os.path.join(path, formatting)


class Uploads(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image_identifier = models.AutoField(primary_key=True)
    title = models.TextField()
    image = models.ImageField(upload_to=update_filename)

    def __str__(self):
        return self.title


class Upvotes(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    upvoter = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='upload_upvoter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)


class Downvotes(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    downvoter = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='upload_downvoter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)


class Favorites(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    favoriter = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='upload_favoriter')
    photo = models.ForeignKey(Uploads, on_delete=models.CASCADE)
