from django.db import models
from player.models import Player
from team.models import Team
from articles.models import Article
from user.models import User

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=250, default=' ')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)

