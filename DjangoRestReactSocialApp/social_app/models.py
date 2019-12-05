from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Profile(TimestampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if instance and created:
            instance.profile = Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(TimestampedModel):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.blog, self.title)


class Comment(TimestampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return '{} - {}'.format(self.post, self.comment)
