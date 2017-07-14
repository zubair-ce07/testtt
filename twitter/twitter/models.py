from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.


class TweetManager(models.Manager):
    def filler_by_username(self, username):
        user = User.objects.get(username__iexact=username)
        return self.filter(user=user).order_by('-pub_date')

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField('published date', auto_now_add=True)
    objects = TweetManager()

    def __str__(self):
        return self.tweet_text
