from django.db import models
from blog.models import Blog
from django.contrib.auth.models import User


class Comment(models.Model):
    text = models.TextField()
    comment_for = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.text + self.created_by.username
