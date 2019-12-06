from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()


class Publisher(User):
    """Model representing an author."""
    company_name = models.CharField(db_index=True, max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)

    class Meta:
        ordering = ['username', 'company_name', ]

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('publisher-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.company_name


@receiver(post_save, sender=Publisher)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
