from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=200)
    category_name = models.CharField(max_length=30)
    category_source = models.CharField(max_length=30)
    publication_date = models.DateField()
    tags = models.TextField()
    detail = models.TextField()
