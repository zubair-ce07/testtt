import os
from sys import path
from django.utils.text import slugify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.append(BASE_DIR + '/news/news_scrappers')
SCRAPY_SETTINGS_PATH = "news_scrappers.settings"

THE_NEWS = 'The News'
DAWN_NEWS = 'Dawn News'
SPIDER_NAMES = {THE_NEWS: slugify(THE_NEWS),
                DAWN_NEWS: slugify(DAWN_NEWS)}