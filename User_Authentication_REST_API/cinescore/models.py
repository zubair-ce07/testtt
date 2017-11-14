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
    category = models.ManyToManyField(Category, related_name='category')
    title = models.CharField(max_length=75)
    date_of_release = models.CharField(max_length=12)
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
    provider_website = models.ForeignKey(Website, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    target_url = models.URLField(max_length=200)

    def __str__(self):
        return self.movie.title


class UserRating(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = (('user', 'movie'),)

    def __str__(self):
        return str(self.user.username)


class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.user.username

