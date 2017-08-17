from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as AuthUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from rest_framework.authtoken.models import Token


class ProfileDoestExist(Http404):
    def __init__(self, username):
        super().__init__("{username} does not exist".format(username=username))


class UserManager(AuthUserManager):
    def get_by_username(self, username):
        try:
            return User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise ProfileDoestExist(username)


class TweetManager(models.Manager):
    def filler_by_username(self, username):
        user = User.objects.get_by_username(username)
        return self.filter(user=user)


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)
    objects = UserManager()

    class Meta:
        db_table = 'User'


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField('published date', auto_now_add=True)
    objects = TweetManager()

    def __str__(self):
        return self.tweet_text

    class Meta:
        db_table = 'tweet'
        ordering = ('-pub_date',)
