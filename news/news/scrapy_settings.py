__author__ = 'luqman'


import os
from sys import path


current_path = os.getcwd()
path.append(str(current_path) + '/the_news/news_scrappers')
SCRAPY_SETTINGS = {
    'BOT_NAME': 'news_scrappers',
    'SPIDER_MODULES': ['news_scrappers.spiders'],
    'NEWSPIDER_MODULE': 'news_scrappers.spiders',
    'ROBOTSTXT_OBEY': True,
    'ITEM_PIPELINES': {
        'news_scrappers.pipelines.NewsScrappersPipeline': 300,
    },
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 5,
    'AUTOTHROTTLE_MAX_DELAY': 60,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    'AUTOTHROTTLE_DEBUG': False,

}
CRAWLER_STATE = False
CRAWLER_NAME = None
CRAWLER_THREAD = None