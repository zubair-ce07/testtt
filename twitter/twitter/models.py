from django.contrib.auth.models import AbstractUser, UserManager as AuthUserManager
from django.http import Http404
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class ProfileDoestExist(Http404):
    def __init__(self,username):
        super().__init__("{username} does not exist".format(username=username))


class UserManager(AuthUserManager):
    def get_by_username(self,username):
        try:
            return User.objects.get(username__iexact=username)
        except ObjectDoesNotExist:
            raise ProfileDoestExist(username)


class TweetManager(models.Manager):
    def filler_by_username(self, username):
        user = User.objects.get_by_username(username)
        return self.filter(user=user).order_by('-pub_date')


class NewsManager(models.Manager):
    def truncate(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM "{0}"'.format(self.model._meta.db_table))
            cursor.execute('VACUUM;')

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)
    objects = UserManager()


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField('published date', auto_now_add=True)
    objects = TweetManager()

    def __str__(self):
        return self.tweet_text


class News(models.Model):
    title = models.CharField(max_length=200)
    content =  models.CharField(max_length=1000)
    publisher =models.ForeignKey(User, blank=True, null=True)
    pub_date = models.DateTimeField('published date', auto_now_add=True)
    image = models.ImageField(null=True)
    image_url = models.URLField(null=True)
    objects = NewsManager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
