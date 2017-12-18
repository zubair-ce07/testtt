from django.db import models


class Review(models.Model):
    movie_id = models.IntegerField()
    comment = models.TextField()
    rating = models.FloatField()
