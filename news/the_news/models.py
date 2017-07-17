# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy, reverse
from django.db import models
from django.utils.html import mark_safe
from django.conf import settings as crawler_settings
# Create your models here.


class NewsPaper(models.Model):
    name = models.CharField(max_length=50)
    source_url = models.URLField(unique=True)
    spider_name = models.CharField(max_length=20)

    def crawler_button(self):
        button = "<button onclick=\"location.href='{}'\" type=\"button\" {}>{}</button>"
        button_state = 'enabled'
        url_name = 'the_news:{}'

        if crawler_settings.CRAWLER_STATE:
            url_name = url_name.format('terminate_fetch_news')
            button_text = 'Terminate Crawling'
            if not crawler_settings.CRAWLER_NAME == self.spider_name:
                button_state = 'disabled'
        else:
            url_name = url_name.format('fetch_news')
            button_text = 'Start Crawling'

        return mark_safe(button.format(reverse(url_name, kwargs={'spider_name': self.spider_name}),
                                       button_state, button_text))

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

        return ("{} {}".format(self.title, str(self.date))).encode('utf-8')

    class Meta:
        verbose_name_plural = "News"
