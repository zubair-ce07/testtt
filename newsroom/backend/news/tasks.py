from __future__ import absolute_import, unicode_literals

from contextlib import contextmanager
from celery import shared_task
from celery.five import monotonic
from django.conf import settings
from django.core.cache import cache
from backend.news.models import Scrapper
from services.scraping.news_scrappers.scrappers import run_scrapy_project


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