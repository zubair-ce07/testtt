# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BasicInformation(models.Model):
    name = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField()
    contact_number = models.IntegerField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Experience(models.Model):
    organization = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField(null=True)
    job_description = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization


class Education(models.Model):
    degree = models.CharField(max_length=30)
    institute = models.CharField(max_length=100)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField(null=True)
    city = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.degree


class Skill(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hobby(models.Model):
    hobby = models.CharField(max_length=30)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)
    description = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.hobby


class Reference(models.Model):
    reference = models.CharField(max_length=30)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference


'''
from cv_maker_app.models import Skill
from cv_maker_app.models import Hobby
from cv_maker_app.models import Reference
import datetime
from cv_maker_app.models import Experience
from cv_maker_app.models import BasicInformation
from cv_maker_app.models import Education
'''