from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Genre(models.Model):
    name = models.CharField(max_length=15)


class Date(models.Model):
    day = models.PositiveSmallIntegerField(null=True, blank=True)
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveSmallIntegerField()


class Image(models.Model):
    BACKDROP = 1
    POSTER = 2
    PROFILE = 3

    TYPES = (
        (BACKDROP, 'Backdrop'),
        (POSTER, 'Poster'),
        (PROFILE, 'Profile'),
    )

    aspect_ratio = models.FloatField(blank=True, null=True)
    file_path = models.CharField(max_length=40, unique=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    iso_639_1 = models.CharField(max_length=2, blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    type = models.PositiveSmallIntegerField(choices=TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Person(models.Model):
    UNKNOWN = 0
    FEMALE = 1
    MALE = 2

    GENDERS = (
        (UNKNOWN, '---'),
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )

    adult = models.NullBooleanField()
    biography = models.TextField(null=True, blank=True)
    birthday = models.OneToOneField(Date, on_delete=models.CASCADE, null=True, blank=True, related_name='birthday')
    deathday = models.OneToOneField(Date, on_delete=models.CASCADE, null=True, blank=True, related_name='deathday')
    gender = models.PositiveSmallIntegerField(choices=GENDERS)
    homepage = models.CharField(max_length=200, null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=200, null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    images = GenericRelation(Image, related_query_name='person')


class Movie(models.Model):
    adult = models.BooleanField(default=False)
    budget = models.BigIntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='movies')
    homepage = models.TextField(null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True)
    original_language = models.CharField(max_length=30)
    original_title = models.CharField(max_length=200)
    overview = models.TextField(null=True, blank=True)
    popularity = models.FloatField(default=0)
    release_date = models.OneToOneField(Date, on_delete=models.CASCADE, null=True, blank=True)
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    tag_line = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    images = GenericRelation(Image, related_query_name='movie')
    cast = models.ManyToManyField(Person, through='Role', related_name='roles')
    crew = models.ManyToManyField(Person, through='Job', related_name='jobs')
    recommendations = models.ManyToManyField('Movie', related_name='recommended', symmetrical=False)


class Role(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character = models.TextField()
    credit_id = models.CharField(max_length=40, unique=True)
    order = models.PositiveSmallIntegerField()


class Job(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    credit_id = models.CharField(max_length=40, unique=True)
    job = models.CharField(max_length=100)


class Video(models.Model):
    TRAILER = 'Trailer'
    TEASER = 'Teaser'
    CLIP = 'Clip'
    FEATURETTE = 'Featurette'

    TYPES = (
        (TRAILER, 'Trailer'),
        (TEASER, 'Teaser'),
        (CLIP, 'Clip'),
        (FEATURETTE, 'Featurette'),
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tmdb_id = models.CharField(max_length=40, unique=True)
    iso_639_1 = models.CharField(max_length=2)
    iso_3166_1 = models.CharField(max_length=2)
    key = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    site = models.CharField(max_length=40)
    size = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPES)
