# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as get_text


class Technology(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    completion_status = models.BooleanField(default=False)
    technology_used = models.ForeignKey(Technology)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="trainee_images/",
                                default="default.png")

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):



class Trainer(models.Model):
    user = models.OneToOneField(User)

    # def __str__(self):
    #     return self.user.user_profile.name


class Trainee(models.Model):
    user = models.OneToOneField(User)
    assignments = models.ManyToManyField(Assignment)
    trainer = models.ForeignKey(Trainer, related_name="trainees", null=True)

    # def __str__(self):
    #     return self.user.user_profile.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    import pdb; pdb.set_trace()
    if created:
        user = UserProfile.objects.create(user=instance.user,
                                          name=instance.user.first_name,
                                          picture=instance.picture)
        Trainer.objects.create(user=instance)
