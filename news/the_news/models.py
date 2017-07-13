# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy,reverse
from django.db import models
from django.utils.html import mark_safe
import the_news.settings as crawler_settings
# Create your models here.


class NewsPaper(models.Model):
    name = models.CharField(max_length=50)
    source_url = models.URLField(unique=True)
    spider_name = models.CharField(max_length=20)

    def crawler(self):
        if not crawler_settings.CRAWLER_STATE:
            return mark_safe('<button onclick="location.href=\'' + reverse('the_news:fetch_news') + '?spider_name=' + self.spider_name + '\'" type="button">Start Crawling</button>')
        else:
            if crawler_settings.CRAWLER_NAME == self.spider_name:
                return mark_safe('<button onclick="location.href=\'' + reverse('the_news:terminate_fetch_news') + '?spider_name=' + self.spider_name + '\'" type="button">Terminate Crawling</button>')
            else:
                return 'Another Crawler is Already Running'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "News Paper"


class News(models.Model):
    title = models.TextField()
    date = models.DateField()
    source_url = models.URLField(unique=True)
    image_url = models.URLField()
    abstract = models.TextField()
    detail = models.TextField()
    news_paper = models.ForeignKey(NewsPaper, on_delete=models.CASCADE)

    def __str__(self):

        return ("{} {}".format(self.title,str(self.date))).encode('utf-8')

    class Meta:
        verbose_name_plural = "News"
