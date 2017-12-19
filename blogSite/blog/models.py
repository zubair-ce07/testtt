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
        post_likes = self.likes.values('post_id').annotate(count=Sum('vote'))
        return post_likes.get()['count']

    def comment_likes(self):
        comments = self.comments.all()
        c_likes = {}
        for comment in comments:
            likes = comment.likes.values('comment_id').annotate(count=Sum('vote'))
            c_likes[likes[0]['comment_id']] = likes[0]['count']

        return c_likes


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(User)


class LikeComment(models.Model):
    vote_choice = (
        (1, 'up_vote'),
        (-1, 'down_vote'),
    )

    vote = models.IntegerField(vote_choice, default=-1)
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment, related_name='likes')
    created_at = models.DateTimeField()


class LikePost(models.Model):
    vote_choice = (
        (1, 'up_vote'),
        (-1, 'down_vote'),
    )
    vote = models.IntegerField(vote_choice, default=-1)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='likes')
    created_at = models.DateTimeField()
