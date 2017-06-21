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
    # due_date = models.DateTimeField("20-3-2012")
    completion_status = models.BooleanField(default=False)
    technology_used = models.ForeignKey(Technology)

    def __str__(self):
        return self.title


class Trainee(models.Model):
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=200)
    assignments = models.ManyToManyField(Assignment)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=200)
    assignments = models.ManyToManyField(Assignment)
    trainee = models.ForeignKey(Trainee)

    def __str__(self):
        return self.name
