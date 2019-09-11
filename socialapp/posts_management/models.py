from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from user_management.models import UserProfile, SocialGroup


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(SocialGroup, default=None, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class TextPost(Post):
    text = models.TextField()


class Picture(models.Model):
    def get_image_filename(self, instance):
        return "post_images/{}_{}".format(instance.post.id, instance.post.created_at)

    image = models.ImageField(upload_to=get_image_filename)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class EventPost(Post):
    event_datetime = models.DateField(default=datetime.now())
    description = models.TextField()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
