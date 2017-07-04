from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)
    following = models.ManyToManyField('self', blank=True)
    followed_by = models.ManyToManyField('self', blank=True)
    # posts = models.ManyToManyField('Post', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['pk']


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.like_timestamp)+' '+self.user.username


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.text