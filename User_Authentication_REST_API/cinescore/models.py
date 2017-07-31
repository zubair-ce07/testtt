from django.db import models
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from User_Authentication import settings


class Category(models.Model):
    category_name = models.CharField(max_length=15)

    def __str__(self):
        return self.category_name


class Movie(models.Model):
    movie_id = models.CharField(max_length=12, unique=True)
    category = models.ManyToManyField(Category, related_name='Movie')
    title = models.CharField(max_length=75)
    date_of_release = models.DateField(max_length=12)
    poster = models.URLField(max_length=400, null=True)
    content_rating = models.CharField(max_length=7)
    plot = models.TextField()

    def __str__(self):
        return self.title


class Website(models.Model):
    url = models.URLField(max_length=100, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    website_base_url = models.ForeignKey(Website, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    website_url = models.URLField(max_length=200)

    def __str__(self):
        return self.movie.title


class UserRating(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    movie = models.ManyToManyField(Movie)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.rating)


class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    movies = models.ManyToManyField(Movie)

