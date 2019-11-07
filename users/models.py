""" It is model shows table structure of Order, products and users."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """ class to add built in auth functionality. """
    phone = models.CharField(max_length=12, default='', \
        validators=[
            RegexValidator(
                regex='^[\d]{4}-[\d]{7}$',
                message=(u"Format should be 1234-1234567"),
                )
            ])
    address = models.CharField(max_length=100, default='')
    USER_ROLES = (
        ('Buyer', 'Buyer'),
        ('Manager', 'Manager'),
    )
    STATUS_TYPES = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    )
    role = models.CharField(max_length=50, choices=USER_ROLES, default='buyer')
    status = models.CharField(max_length=50, choices=STATUS_TYPES, default='Not Approved')


    def __str__(self):
        return self.username

