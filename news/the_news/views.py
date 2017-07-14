# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urlparse
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import generics
from scrappers import CrawlSpiderThread, run_scrapy_project, initialize_spiders
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from models import News, NewsPaper
from serializers import NewsSerializer


class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'the_news/news_list.html'

    def get(self, request, *args, **kwargs):
        news_list = News.objects.all()
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

        return render(request, self.template_name, {'news_list': news_list})


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news_object'


class FetchView(View):
    scrapy_spiders_status = {}
    scrapy_spiders_thread = {}
    scrapy_spiders_status['the-news']=False
    scrapy_spiders_status['dawn-news']=False
    scrapy_spiders_thread['the-news'] = None
    scrapy_spiders_thread['dawn-news'] = None

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(FetchView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        spider_name = kwargs['spider_name']
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
        url = request.META.get('HTTP_REFERER',reverse('the_news:main'))
        url = urlparse.urljoin(url, urlparse.urlparse(url).path)
        url = "{}?message={}".format(url,message)

        return redirect(url)

class TerminateView(View):
    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(TerminateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        spider_name = kwargs['spider_name']
        if not spider_name:
            message = 'Provide Spider Name'
        else:
            if FetchView.scrapy_spiders_status.has_key(spider_name) and FetchView.scrapy_spiders_thread[spider_name].isAlive():
                    FetchView.scrapy_spiders_thread[spider_name].stop()
                    FetchView.scrapy_spiders_status[spider_name] = False
                    message = spider_name + ' Spider Successfully Terminated'

            else:
                message = spider_name + ' Spider Not Crawling. Start Spider First'
        url = request.META.get('HTTP_REFERER',reverse('the_news:main'))
        url = urlparse.urljoin(url, urlparse.urlparse(url).path)
        url = "{}?message={}".format(url, message)

        return redirect(url)
class TheNewsMainView(View):
    template_name = 'the_news/main.html'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, *args, **kwargs):
        return super(TheNewsMainView, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
            return render(request, self.template_name,{'scrapy_spider_status': FetchView.scrapy_spiders_status, 'message':request.GET.get('message','')})

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailsAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer