from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    '''
    Extension of the User model to include employee data
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=32)
    supervisor = models.ForeignKey("self", blank=True, null=True)
    