"""Customer models module."""
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Cutomer model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """Return model in string."""
        return f'{self.user.username} Profile'

    def _get_full_name(self):
        """Return the person's full name."""
        return '%s %s' % (self.user.first_name, self.user.last_name)

    full_name = property(_get_full_name)
