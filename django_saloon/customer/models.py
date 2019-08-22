from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SaloonUser(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_saloon = models.BooleanField('saloon status', default=False)


class Customer(models.Model):
    user = models.OneToOneField(SaloonUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
