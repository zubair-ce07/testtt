from __future__ import unicode_literals
from django.db import models


class Video(models.Model):
    owner = models.ForeignKey('auth.User', related_name='videos',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, default='')

    def __str__(self):
        return self.name
