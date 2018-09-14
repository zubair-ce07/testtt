from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    writer = models.ForeignKey(
        'auth.User', related_name='blogs', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()
    writer = models.ForeignKey(
        'auth.User', related_name='comments', on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.body
