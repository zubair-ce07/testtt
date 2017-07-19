from django.contrib.auth.models import User
from django.db import models

import datetime


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, default='', blank=True)
    address = models.CharField(max_length=150, default='', blank=True)
    date_of_birth = models.DateField(blank=True)
    gender = models.CharField(max_length=1, error_messages={'error': 'Invalid Gender'}, blank=True)
    image = models.ImageField(upload_to='./user-images/', default='user.png', blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(),blank=True)


class Blog(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
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
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()

