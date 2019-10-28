"""
Module for custom user.

This module has initialization of
custom user which extends Abstract User
with extra fields.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book




class UserProfile(AbstractUser):
    """User profile class.

    This class initializes attributes for user
    in addition to Abstract user fields.
    """
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    book_count = models.IntegerField(default=0)
   
    def __str__(self):
        return self.email

