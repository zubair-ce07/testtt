from django.db import models
from django.utils import timezone
from web.users.models import Address


class Post(models.Model):

    posted_by = models.ForeignKey('users.User', related_name='posts')
    title = models.CharField(max_length=255)
    area = models.DecimalField(decimal_places=3, max_digits=100)
    location = models.OneToOneField(Address)
    description = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    demanded_price = models.DecimalField(decimal_places=3, max_digits=100)
    is_sold = models.BooleanField(default=False)
    sold_on = models.DateTimeField(default='')
    posted_on = models.DateTimeField(default=timezone.now)
    expired_on = models.DateTimeField()


class Picture(models.Model):

    post = models.ForeignKey('Post', related_name='pictures')
    url = models.CharField(max_length=1024)
    is_expired = models.BooleanField(default=False)


class Request(models.Model):

    post = models.ForeignKey('Post', related_name='requests')
    message = models.CharField(max_length=512)
    price = models.DecimalField(decimal_places=3, max_digits=100)
    status = models.CharField(max_length=255, default='pending')
    requested_on = models.DateTimeField(default=timezone.now)


class PostView(models.Model):

    viewed_by = models.ForeignKey('users.User', related_name='views')
    post_viewed = models.ForeignKey('posts.Post', related_name='post_views')
    viewed_on = models.DateTimeField(default=timezone.now)





