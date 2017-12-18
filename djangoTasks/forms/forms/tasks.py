from __future__ import absolute_import, unicode_literals

import os
import subprocess
import logging

from celery.task import task


log = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@task(name='get_thenews_article_every_minutes')
def get_thenews_article_every_minutes():
    os.chdir(os.path.join(BASE_DIR+'/newsscrapper/newsscrapper'))
    subprocess.call("ls -l", shell=True)
    subprocess.call(["scrapy", "crawl", "newsscrapper"])
    return True
