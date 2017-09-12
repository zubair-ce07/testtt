from django.utils.timezone import localdate
from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    slug = models.SlugField()
    text = models.TextField()
    summary = models.TextField()
    created_on = models.DateField(default=localdate)
    is_published = models.BooleanField(default=True)
    comments_allowed = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    published_date = models.DateField(default=localdate, blank=True)

    def __str__(self):
        return self.title
