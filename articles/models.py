from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100, default='Title')
    author = models.CharField(max_length=50, default='Author')
    description = models.CharField(max_length=100, default='Description')
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.title