from django.db import models
from django.contrib.auth.models import User


class UserStatus(models.Model):
    status_text = models.CharField(max_length=200)
    status_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_status')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.status_text


class UserFollowers(models.Model):
    followee = models.ForeignKey(User, related_name="followee")
    follower = models.ForeignKey(User, related_name="followers")

    class Meta:
        unique_together = ('followee', 'follower')
        verbose_name_plural = "UserFollowers"

