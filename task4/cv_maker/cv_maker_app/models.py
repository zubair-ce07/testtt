# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class BasicInformation(models.Model):
    user_id = models.IntegerField()
    image = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    contact_number = models.IntegerField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=50)
    skill_level = (('1', "Beginner"),
                   ('2', "Little Knowledge"),
                   ('3', "Intermediate"),
                   ('4', "Advance"),
                   ('5', "Expert")
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
    user_id = models.IntegerField()
    organization = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    starting_date = models.DateField()
    ending_date = models.DateField(null=True)
    job_description = models.CharField(max_length=255)
    city = models.CharField(max_length=30)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization


class Education(models.Model):
    user_id = models.IntegerField()
    degree = models.CharField(max_length=30)
    institute = models.CharField(max_length=100)
    starting_date = models.DateField()
    ending_date = models.DateField(null=True)
    city = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    person = models.ForeignKey(BasicInformation, on_delete=models.CASCADE)

    def __str__(self):
        return self.degree


class Job(models.Model):
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    experience = models.IntegerField()
    description = models.CharField(max_length=1024)
    skill1 = models.CharField(max_length=30, null=True)
    skill2 = models.CharField(max_length=30, null=True)
    skill3 = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.title
