from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Creating this class to add extra fields if required in future"""
    def __str__(self):
        """String for representing the Model object."""
        return self.username
