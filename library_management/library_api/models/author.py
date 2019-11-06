from django.db import models
from django.urls import reverse

from .custom_user import CustomUser as User


class Author(User):
    """Model representing an author."""
    phone = models.CharField(max_length=11, blank=True)

    class Meta:
        ordering = ['username', 'first_name', ]

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.get_full_name()
