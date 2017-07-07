# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class NewsPaper(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "News Paper"


class News(models.Model):
    title = models.TextField()
    date = models.DateField()
    news_url = models.URLField(unique=True)
    image_url = models.URLField()
    abstract = models.TextField()
    detail = models.TextField()
    news_paper = models.ForeignKey(NewsPaper, on_delete=models.CASCADE)

    def __str__(self):
        return (self.title + " " + str(self.date)).encode('utf-8')

    class Meta:
        verbose_name_plural = "News"
