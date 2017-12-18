from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    modified_at = models.DateTimeField()
    body = models.TextField()
    author = models.OneToOneRel(Person)
    category = models.ForeignKey(Category)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    body = models.TextField()
    created_at = models.DateTimeField()
    user = models.OneToOneRel(Person)


class Likes(models.Model):
    vote_choice = (
        (0, 'up_vote'),
        (1, 'down_vote'),

    )
    vote = models.IntegerField(vote_choice, default=-1)
    user = models.OneToOneRel(Person)
    comment = models.ForeignKey(Comment)
    created_at = models.DateTimeField()


class Person(AbstractUser):
    person = models.OneToOneField(AbstractUser)

