from django.db import models
from django.conf import settings


class Articles(models.Model):
    title = models.CharField(max_length=200)
    category_name = models.CharField(max_length=30)
    category_source = models.CharField(max_length=30)
    publication_date = models.DateField()
    tags = models.TextField()
    detail = models.TextField()
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="articles",
        null = True, blank=True
    )
