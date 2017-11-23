from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    modified_at = models.DateTimeField()
    body = models.TextField()
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    def post_likes(self):
        post_likes = Like_post.objects.filter(post_id=self.id).values('post_id').annotate(count=Sum('vote'))
        return post_likes.get()['count']

    def comment_likes(self):
        comment_likes = Like_comment.objects.filter(comment__post_id=self.id).values('comment_id').annotate(count=Sum('vote'))
        c_likes = {}
        for comment in comment_likes:
            c_likes[comment['comment_id']] = comment['count']

        return c_likes


class Comment(models.Model):
    post = models.ForeignKey(Post)
    body = models.TextField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(User)


class Like_comment(models.Model):
    vote_choice = (
        (1, 'up_vote'),
        (-1, 'down_vote'),
    )

    vote = models.IntegerField(vote_choice, default=-1)
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    created_at = models.DateTimeField()


class Like_post(models.Model):
    vote_choice = (
        (1, 'up_vote'),
        (-1, 'down_vote'),
    )
    vote = models.IntegerField(vote_choice, default=-1)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField()
