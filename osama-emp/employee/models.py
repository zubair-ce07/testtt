from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
# Create your models here.


class Employee(models.Model):
    '''
    Extension of the User model to include employee data
    '''

    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField()
    job_title = models.CharField(max_length=32)
    reports_to = models.ForeignKey("self",
                                   blank=True,
                                   null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    is_active = models.BooleanField(default=True)
    date_of_joining = models.DateField()
    nationality = models.CharField(max_length=32)
