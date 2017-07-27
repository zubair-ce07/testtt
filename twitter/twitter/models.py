from django.contrib.auth.models import AbstractUser, UserManager as AuthUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class ProfileDoestExist(Http404):
    def __init__(self, username):
        super().__init__("{username} does not exist".format(username=username))


class UserManager(AuthUserManager):
    def get_by_username(self, username):
        try:
            return User.objects.get(username__iexact=username)
        except ObjectDoesNotExist:
            raise ProfileDoestExist(username)


class TweetManager(models.Manager):
    def filler_by_username(self, username):
        user = User.objects.get_by_username(username)
        return self.filter(user=user).order_by('-pub_date')


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
