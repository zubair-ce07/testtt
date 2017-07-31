from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View

from news.models import Scrapper
from news.scarppers import CrawlSpiderThread, run_scrapy_project

# Create your views here.


class FetchView(View):
    scrapy_thread = None

    def get(self, request, *args, **kwargs):
        scrappers = Scrapper.objects.values('name')

        if not FetchView.scrapy_thread or not FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread = CrawlSpiderThread(scrappers,
                                settings.SCRAPY_SETTINGS_PATH,
                                run_scrapy_project)
            FetchView.scrapy_thread.start()

        return redirect('home')


class TerminateView(View):
    def get(self, request, *args, **kwargs):
        if FetchView.scrapy_thread and FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread.stop()
        return redirect('home')

class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/home.html')
