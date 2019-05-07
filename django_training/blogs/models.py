from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    blog_description = models.TextField()
    published_date = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog_title
