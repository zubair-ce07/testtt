from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=500)
    date = models.DateField()
