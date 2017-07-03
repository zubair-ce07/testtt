from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField()
    user_name = models.CharField(max_length=30, unique=True, null=False)
    # followed_by = models.ForeignKey('self', on_delete=models.CASCADE)
    password = models.CharField(max_length=50, null=False)
    following = models.ForeignKey('self', on_delete=models.CASCADE)
    posts = models.ForeignKey('Post', on_delete=models.DO_NOTHING)


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like_timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=150, null=False)