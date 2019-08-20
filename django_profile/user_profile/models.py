"""User Profile Models module.

This is user profile models module it has differnet model for the user profile app.
"""
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Customized user Model.

    This is customized user model for user profile app, it inherit
    the AbstractUser,add different fields to it and override it's
    username field from username to email.
    """
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, error_messages={
        'unique': _("A user with that email already exists."),
    })
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True, choices=gender_choices,
                              default='male',)
    phone_no = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ['username']
