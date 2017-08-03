# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

GENRE_CHOICES = [
    ('Novel', 'Novel'),
    ('Thriller', 'Thriller'),
    ('Drama', 'Drama'),
    ('Biograpghy', 'Biograghy'),
    ('Text Book', 'Text Book'),
    ('Science', 'Science'),
    ('Not Specified', 'Not Specified'),
]


@python_2_unicode_compatible
class Publisher(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=32)
    email = models.EmailField()
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=32)
    email = models.EmailField()
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(max_length=512)
    genre = models.CharField(max_length=64, choices=GENRE_CHOICES, default='Not Specified')
    publisher = models.ForeignKey(Publisher)
    authors = models.ManyToManyField(Author)
    pub_date = models.DateField(default=datetime.now().strftime("%d.%m.%Y"))

    def __str__(self):
        return self.title
