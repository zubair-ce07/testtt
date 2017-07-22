from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    slug = models.SlugField()
    text = models.TextField()
    summary = models.TextField()
    created_on = models.DateField()
    is_published = models.BooleanField(default=False)
    comments_allowed = models.BooleanField(default=True)
    is_public = models.BooleanField()

