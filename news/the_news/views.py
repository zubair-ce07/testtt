# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urlparse
from rest_framework import generics
from scrappers import CrawlSpiderThread
from scrappers import run_scrapy_project
from models import News, NewsPaper
from serializers import NewsSerializer
from messages import SpiderMessages
from decorators import ip_check
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.conf import settings


class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'the_news/news_list.html'

    @method_decorator(ip_check(ip_list=['127.0.0.1']))
    def dispatch(self, *args, **kwargs):
        return super(NewsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        filter_val = self.request.GET.get('query')
        if filter_val:
            query = News.objects.filter(Q(title__icontains=filter_val) |
                                       Q(detail__icontains=filter_val) |
                                       Q(abstract__icontains=filter_val))
        else:
            query = News.objects.all()

        return query.order_by('-date')

    def get(self, request, *args, **kwargs):
        news_list = self.get_queryset()
        context = {'query': request.GET.get('query','')}

        if news_list:
            paginator = Paginator(news_list, 20)
            page = kwargs.get('page', 1)
            try:
                news_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                news_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                news_list = paginator.page(paginator.num_pages)
            context['news_list'] = news_list
        else:
            context['message'] = 'No news found'

        return render(request, self.template_name, context)


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news_object'


class FetchView(View):
    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(FetchView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        spider_name = kwargs['spider_name']
        if settings.CRAWLER_STATE:
            message = SpiderMessages.RUNNING.format(spider_name)
        else:
            if spider_name:
                news_paper = NewsPaper.objects.filter(spider_name=spider_name).first()

                if news_paper:
                    settings.CRAWLER_THREAD = CrawlSpiderThread(news_paper.spider_name,
                                                                'news_scrappers.settings',
                                                                settings.SCRAPY_SETTINGS,
                                                                run_scrapy_project)
                    settings.CRAWLER_THREAD.start()
                    message = SpiderMessages.SUCCESSFUL_START.format(
                        spider_name)
                else:
                    message = SpiderMessages.NOT_EXISTS.format(spider_name)
            else:
                message = SpiderMessages.MISSING_SPIDER_NAME
        url = request.META.get('HTTP_REFERER', reverse('the_news:main'))
        url = urlparse.urljoin(url, urlparse.urlparse(url).path)
        url = "{}?message={}".format(url, message)

        return redirect(url)


class TerminateView(View):
    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(TerminateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        spider_name = kwargs.get('spider_name', '')
        if spider_name:
            if settings.CRAWLER_NAME and settings.CRAWLER_NAME == spider_name and settings.CRAWLER_THREAD.isAlive():
                settings.CRAWLER_THREAD.stop()
                message = SpiderMessages.SUCCESSFUL_TERMINATION.format(
                    spider_name)
            else:
                message = SpiderMessages.NOT_RUNNING.format(spider_name)
        else:
            message = SpiderMessages.MISSING_SPIDER_NAME

        url = request.META.get('HTTP_REFERER', reverse('the_news:main'))
        url = urlparse.urljoin(url, urlparse.urlparse(url).path)
        url = "{}?message={}".format(url, message)

        return redirect(url)


class TheNewsMainView(View):
    template_name = 'the_news/main.html'
    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(TheNewsMainView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        news_papers = NewsPaper.objects.all()
        scrapy_spider_state = dict()
        for news_paper in news_papers:
            if settings.CRAWLER_NAME and settings.CRAWLER_NAME == news_paper.spider_name:
                scrapy_spider_state[news_paper.spider_name] = True
            else:
                scrapy_spider_state[news_paper.spider_name] = False

        return render(request, self.template_name, {'scrapy_spider_status': scrapy_spider_state,
                                                    'crawler_state': settings.CRAWLER_STATE,
                                                    'message': request.GET.get('message', '')})


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailsAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
