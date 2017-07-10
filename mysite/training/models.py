# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.db.models import Count


class Technology(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    completion_status = models.BooleanField(default=False)
    technology_used = models.ManyToManyField(Technology)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="user_images/",
                                default="default.png")

    def __str__(self):
        return self.name


class TrainerManager(models.Manager):
    def available_trainer(self):
        trainees_count = self.model.objects.annotate(num_trainees=Count(
                                                     'trainees'))
        trainees_lt_3 = trainees_count.filter(num_trainees__lt=3)
        if trainees_lt_3:
            return trainees_lt_3.order_by('num_trainees')[0]


class Trainer(models.Model):
    user = models.OneToOneField(User, related_name='trainer')
    objects = TrainerManager()

    def __str__(self):
        return self.user.user_profile.name


class Trainee(models.Model):
    user = models.OneToOneField(User, related_name='trainee')
    assignments = models.ManyToManyField(Assignment)
    trainer = models.ForeignKey(Trainer, related_name="trainees", null=True)

    def __str__(self):
        return self.user.user_profile.name
