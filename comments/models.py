from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='comments', blank=True, null=True, on_delete=models.SET_NULL)
    player = models.ForeignKey('teams.Player', related_name='comments', blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey('teams.Team', related_name='comments', blank=True, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey('articles.Article', related_name='comments', blank=True, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=250, default=' ')


class Follow(models.Model):
    # Read about related names and add them in foreign keys.
    user = models.ForeignKey(get_user_model(), related_name='follows', blank=True, null=True, on_delete=models.CASCADE)
    player = models.ForeignKey('teams.Player', related_name='follows', blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey('teams.Team', related_name='follows', blank=True, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey('articles.Article', related_name='follows', blank=True, null=True, on_delete=models.SET_NULL)

