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


def get_image_filename(instance):
    return "post_images/{}_{}".format(instance.post.id, instance.post.created_at)


class Picture(models.Model):
    image = models.ImageField(upload_to=get_image_filename)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class EventPost(Post):
    date = models.DateField(default='')
    time = models.TimeField(default='')
    description = models.TextField()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
