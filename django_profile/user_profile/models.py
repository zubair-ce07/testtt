from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, error_messages={
        'unique': _("A user with that username already exists."),
    })
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    phone_no = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ['username']
