from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/images/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.blog, self.title)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return '{} - {}'.format(self.post, self.comment)
