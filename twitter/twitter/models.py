from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField('published date', auto_now_add=True)

    def __str__(self):
        return self.tweet_text
