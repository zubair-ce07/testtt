from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=15)


class Movie(models.Model):
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=30, null=True, blank=True)
    budget = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    homepage = models.CharField(max_length=50, null=True, blank=True)
    tmdb_id = models.IntegerField()
    original_language = models.CharField(max_length=15)
    original_title = models.CharField(max_length=50)
    overview = models.TextField(null=True, blank=True)
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=30, null=True, blank=True)
    release_date = models.DateField()
    revenue = models.IntegerField()
    runtime = models.IntegerField()
    status = models.CharField(max_length=15)
    tagline = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=50)
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
