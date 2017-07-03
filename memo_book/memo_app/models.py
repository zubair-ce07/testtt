from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Memory(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField()
    url = models.CharField(max_length=300)
    tags = models.CharField(max_length=200)
    image = models.FileField()