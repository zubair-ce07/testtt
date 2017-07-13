# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import generics
from scrappers import CrawlSpiderThread, run_scrapy_project, initialize_spiders
from django.conf import settings
from django.urls import reverse
# Create your views here.
from the_news.models import News, NewsPaper
from the_news.serializers import NewsSerializer


class FetchView(View):
    scrapy_spiders_status = {}
    scrapy_spiders_thread = {}
    scrapy_spiders_status['the-news']=False
    scrapy_spiders_status['dawn-news']=False
    scrapy_spiders_thread['the-news'] = None
    scrapy_spiders_thread['dawn-news'] = None
    def get(self, request, *args, **kwargs):
        spider_name = request.GET.get('spider_name', '')

        if True in FetchView.scrapy_spiders_status.values():
            message = 'A spider is already running please stop it first'
        else:
            if not spider_name:
                message = 'Provide Spider Name'
            else:
                # if spider name exists in database
                # should be checked
                spider_status = FetchView.scrapy_spiders_status.get(spider_name, False)
                if not spider_status:
                    FetchView.scrapy_spiders_status[spider_name] = False
                if spider_status == False:
                    FetchView.scrapy_spiders_thread[spider_name] = CrawlSpiderThread(spider_name,
                                                                         'news_scrappers.settings',
                                                                         settings.SCRAPY_SETTINGS,
                                                                         run_scrapy_project)
                    FetchView.scrapy_spiders_thread[spider_name].start()
                    FetchView.scrapy_spiders_status[spider_name] = True
                    message = spider_name + ' Successfully Started'
        return redirect(reverse('the_news:main')+'?message='+message)


class TerminateView(View):
    def get(self, request, *args, **kwargs):
        spider_name = request.GET.get('spider_name', '')
        if not spider_name:
            message = 'Provide Spider Name'
        else:
            if FetchView.scrapy_spiders_status.has_key(spider_name) and FetchView.scrapy_spiders_thread[spider_name].isAlive():
                    FetchView.scrapy_spiders_thread[spider_name].stop()
                    FetchView.scrapy_spiders_status[spider_name] = False
                    message = spider_name + ' Spider Successfully Terminated'
            else:
                message = spider_name + ' Spider Not Crawling. Start Spider First'
        return redirect(reverse('the_news:main')+'?message='+message)


class TheNewsMainView(View):
    template_name = 'the_news/main.html'

    def get(self, request, *args, **kwargs):
            return render(request, self.template_name,{'scrapy_spider_status': FetchView.scrapy_spiders_status, 'message':request.GET.get('message','')})

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailsAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer