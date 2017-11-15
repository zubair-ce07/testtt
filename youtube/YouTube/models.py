from __future__ import unicode_literals
from django.db import models


# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     email = models.CharField(max_length=200, unique=True)
#     # channel = models.OneToOneField('Channel', on_delete=models.CASCADE,
#     #                                null=True)
#
#     def __str__(self):
#         return self.username


# class Channel(models.Model):
#     owner = models.OneToOneField('auth.User', related_name='owner',
#                                  on_delete=models.CASCADE)
#     subscriber = models.ManyToManyField('User', related_name='subscriber')


class Video(models.Model):
    owner = models.ForeignKey('auth.User', related_name='videos',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, default='')

    def __str__(self):
        return self.name
    # channel = models.ForeignKey('Channel', on_delete=models.CASCADE)