# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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


class Trainee(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="trainee_images/",
                                default="default.png")
    assignments = models.ManyToManyField(Assignment)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="trainer_images/",
                                default="default.png")
    assignments = models.ManyToManyField(Assignment)
    trainee = models.ForeignKey(Trainee)

    def __str__(self):
        return self.name
