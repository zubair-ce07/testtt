from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Creating this class to add extra fields to user if required in future"""

    def __str__(self):
        """String for representing the user object."""
        return self.username
