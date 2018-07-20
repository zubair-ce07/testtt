from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=50, default=' ')
    ranking = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default='county')
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name
