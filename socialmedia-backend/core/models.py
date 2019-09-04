from django.db import models

from users.models import User


# https://stackoverflow.com/questions/44776488/fields-clash-in-case-of-inheritance
# class DateTimeModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.content}'


class PostMedia(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    file_name = models.FileField(upload_to="posts-media/")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.file_name}'


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.message}'
