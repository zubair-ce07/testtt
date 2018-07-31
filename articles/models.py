from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
from articles.choices import ArticleChoices
from teams.models import Player, Team, Photo
from tinymce import models as tinymce_models


class Article(models.Model):
    title = models.CharField(max_length=100, default=' ')
    author = models.CharField(max_length=50, default=' ')
    description = models.CharField(max_length=100, default=' ')
    category = models.CharField(max_length=10, default=' ', choices=ArticleChoices.Choices)
    url = models.URLField(max_length=100, default=' ')
    # Add a related_players field many to many
    players = models.ManyToManyField(Player, related_name='articles', blank=True)
    teams = models.ManyToManyField(Team, related_name='articles', blank=True)
    content = tinymce_models.HTMLField(default='')
    photos = GenericRelation(Photo, related_query_name='articles')

    def __str__(self):
        return self.title
