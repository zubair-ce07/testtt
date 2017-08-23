from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from backend.news.models import Scrapper
from services.scraping.news_scrappers.scrappers import run_scrapy_project


@shared_task
def start_scraping():
    if settings.SCRAPY_RUNNING:
        return
    else:
        settings.SCRAPY_RUNNING = True
        scrappers = Scrapper.objects.values('name')
        run_scrapy_project(settings.SCRAPY_SETTINGS_PATH,scrappers)
        settings.SCRAPY_RUNNING = False