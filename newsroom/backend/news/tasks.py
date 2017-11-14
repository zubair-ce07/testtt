from __future__ import absolute_import, unicode_literals

from contextlib import contextmanager
from celery import shared_task
from celery.five import monotonic
from django.conf import settings
from django.core.cache import cache
from backend.news.models import Scrapper, News
from services.scraping.news_scrappers.scrappers import run_scrapy_project
from services.analysis.sentimental_classifier import SentimentalClassifier

LOCK_EXPIRE = 60 * 60 * 24  # Lock expires in 24 hours

@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if monotonic() < timeout_at:
            cache.delete(lock_id)

@shared_task
def start_scraping():
    lock_id = 'start_scraping'
    with memcache_lock(lock_id, 'true') as acquired:
        if acquired:
            try:
                scrappers = Scrapper.objects.values('name')
                run_scrapy_project(settings.SCRAPY_SETTINGS_PATH, scrappers)
            finally:
                cache.delete(lock_id)

@shared_task
def start_sentimental_analysis():
    lock_id = 'start_sentimental_analysis'
    with memcache_lock(lock_id, 'true') as acquired:
        if acquired:
            classifier = SentimentalClassifier()
            try:
                classifier.load_classifier(settings.SENTIMENTAL_MODEL_PATH)
            except FileNotFoundError:
                classifier.load_data()
                classifier.train()
                classifier.save_classifier(settings.SENTIMENTAL_MODEL_PATH)
            finally:
                news = News.objects.filter(sentiment=None)
                for news_item in news:
                    if news_item.summary:
                        sentiment = classifier.classify(news_item.summary)
                        if sentiment == 'pos':
                            news_item.sentiment = True
                        else:
                            news_item.sentiment = False
                        news_item.save()
            cache.delete(lock_id)