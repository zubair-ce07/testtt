from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View

from backend.news.models import Scrapper
from services.scraping.news_scrappers.scrappers import CrawlSpiderThread, run_scrapy_project


class FetchView(View):
    scrapy_thread = None

    def get(self, request, *args, **kwargs):
        scrappers = Scrapper.objects.values('name')
        if not FetchView.scrapy_thread or not FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread = CrawlSpiderThread(scrappers,
                                                        settings.SCRAPY_SETTINGS_PATH,
                                                        run_scrapy_project)
            FetchView.scrapy_thread.start()

        return redirect('news:home')


class TerminateView(View):
    def get(self, request, *args, **kwargs):
        if FetchView.scrapy_thread and FetchView.scrapy_thread.isAlive():
            FetchView.scrapy_thread.stop()
        return redirect('news:home')


class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/home.html')
