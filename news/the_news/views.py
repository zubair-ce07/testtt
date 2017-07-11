# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import generics
from scrappers import CrawlSpiderThread, run_scrapy_project
from django.conf import settings
# Create your views here.
from the_news.models import News
from the_news.serializers import NewsSerializer


class FetchView(View):
    scrapy_thread = None

    def get(self, request, *args, **kwargs):
        if not FetchView.scrapy_thread or not FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread = CrawlSpiderThread(
                'the-news', 'news_scrappers.settings', settings.SCRAPY_SETTINGS, run_scrapy_project)
            FetchView.scrapy_thread.start()
        return redirect('the_news:main')


class TerminateView(View):
    def get(self, request, *args, **kwargs):
        if FetchView.scrapy_thread and FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread.stop()
        return redirect('the_news:main')


class TheNewsMainView(View):
    template_name = 'the_news/main.html'

    def get(self, request, *args, **kwargs):
        if not FetchView.scrapy_thread or not FetchView.scrapy_thread.isAlive():
            return render(request, self.template_name)
        return render(request, self.template_name, {'isScraping': FetchView.scrapy_thread.isAlive()})


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailsAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer