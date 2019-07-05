# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BasicInformation(models.Model):
    user_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField()
    contact_number = models.IntegerField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=30, unique=True)
    skill_level = ((1, "Beginner"),
                   (2, "Little Knowledge"),
                   (3, "Intermediate"),
                   (4, "Advance"),
                   (5, "Expert")
                   )
    skill1 = models.CharField(max_length=30, null=True)
    skill2 = models.CharField(max_length=30, null=True)
    skill3 = models.CharField(max_length=30, null=True)
    skill4 = models.CharField(max_length=30, null=True)
    skill5 = models.CharField(max_length=30, null=True)
    skill1_level = models.CharField(max_length=30, null=True, choices=skill_level)
    skill2_level = models.CharField(max_length=30, null=True, choices=skill_level)
    skill3_level = models.CharField(max_length=30, null=True, choices=skill_level)
    skill4_level = models.CharField(max_length=30, null=True, choices=skill_level)
    skill5_level = models.CharField(max_length=30, null=True, choices=skill_level)
    hobby1 = models.CharField(max_length=30, null=True)
    hobby2 = models.CharField(max_length=30, null=True)
    hobby3 = models.CharField(max_length=30, null=True)
    reference1 = models.CharField(max_length=30, null=True)
    reference2 = models.CharField(max_length=30, null=True)

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


'''
import datetime
from cv_maker_app.models import Experience
from cv_maker_app.models import BasicInformation
from cv_maker_app.models import Education

yus = BasicInformation(user_name="ich_bin_yusra", name="Yusra Khalid", date_of_birth=datetime.datetime(1998,11,2),contact_number=3229773430, address="p-56 st no 1, fsd", email="ykhalid.bese16seecs@seecs.edu.pk",skill1="python",skill2="management",skill1_level=1,skill2_level=4, hobby1="Gaming",reference1="facebook.com/yusrakhalid.35")
'''