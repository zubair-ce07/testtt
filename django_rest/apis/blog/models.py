from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField()
    writer = models.ForeignKey(
        'auth.User', related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    comments = GenericRelation('self')

    # Required attributes for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.body


class Blog(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    writer = models.ForeignKey(
        'auth.User', related_name='blogs', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
