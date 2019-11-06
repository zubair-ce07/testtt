from django.db import models
from django.urls import reverse

from .custom_user import CustomUser as User


class Publisher(User):
    """Model representing an author."""
    company_name = models.CharField(db_index=True, max_length=100)
    address = models.CharField(max_length=100, blank=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)

    class Meta:
        ordering = ['username', 'company_name',]

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('publisher-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.company_name
