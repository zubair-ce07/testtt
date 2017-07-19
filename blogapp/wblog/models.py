from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, default='', blank=True)
    address = models.CharField(max_length=150, default='', blank=True)
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, error_messages={'error': 'Invalid Gender'}, blank=True)
    image = models.ImageField(upload_to='user-images', default='user.png', blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    text = models.TextField()
    summary = models.TextField()
    created_on = models.DateField()
    is_published = models.BooleanField(default=False)
    comments_allowed = models.BooleanField(default=True)
    is_public = models.BooleanField()


class Comment(models.Model):
    text = models.TextField()
    comment_for = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()


@receiver(post_save, sender=User)
def save_userinfo(sender, instance, created, **kwargs):
    if created:
        user_info = getattr(instance, 'info', None)
        info = UserInfo(user=instance, phone_no=user_info['phone_num'],
                        address=user_info['address'], date_of_birth=user_info['dob'],
                        gender=user_info['gender'], created_at=user_info['created_at']
                        )
        info.blog_info = user_info
        info.save()


@receiver(post_save, sender=UserInfo)
def save_userblog(sender, instance, created, **kwargs):
    if created:
        blog_info = getattr(instance, 'blog_info', None)

        blog = Blog(created_by=instance.user, slug=blog_info['blog_slug'],
                    text=blog_info['blog_text'], created_on=datetime.datetime.now().date(),
                    is_published=blog_info['blog_is_published'] == 'TRUE',
                    comments_allowed=blog_info['blog_comments_allowed'] == 'TRUE',
                    is_public=blog_info['blog_is_public'] == 'TRUE')
        blog.comment_info = blog_info

        blog.save()


@receiver(post_save, sender=Blog)
def save_blog_comments(sender, instance, created, **kwargs):
    if created:
        comment_info = getattr(instance, 'comment_info', None)
        comment = Comment(comment_for=instance, text=comment_info['comment_text'],
                          created_on=datetime.datetime.now(), created_by=instance.created_by,
                          user_ip=comment_info['ip'])
        comment.save()
