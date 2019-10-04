import time

from django.db import models
from accounts.models import FBUser


def upload_location(instance, filename):
    _, extension = filename.split('.')
    stamp = time.time()
    return 'posts/{}_{}.{}'.format(instance.fb_user.username, stamp, extension)


class Post(models.Model):
    description = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to=upload_location, blank=True)
    fb_user = models.ForeignKey(FBUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
