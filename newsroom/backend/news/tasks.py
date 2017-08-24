from __future__ import absolute_import, unicode_literals

from contextlib import contextmanager
from hashlib import md5
from services.celery import app
from celery.five import monotonic
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.cache import cache
from backend.news.models import Scrapper
from services.scraping.news_scrappers.scrappers import run_scrapy_project


logger = get_task_logger(__name__)

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

@app.task(bind=True)
def start_scraping(self):
    start_scraping_hexdigest = md5('start_scraping'.encode('utf-8')).hexdigest()
    lock_id = '{0}-lock-{1}'.format('start_scraping', start_scraping_hexdigest)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            scrappers = Scrapper.objects.values('name')
            run_scrapy_project(settings.SCRAPY_SETTINGS_PATH, scrappers)