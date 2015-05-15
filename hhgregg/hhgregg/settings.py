# -*- coding: utf-8 -*-

# Scrapy settings for hhgregg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
BOT_NAME = 'hhgregg'
DOWNLOAD_DELAY = 5

HTTPCACHE_IGNORE_HTTP_CODES = range(500, 599)
# HTTPCACHE_DIR = os.environ.get('HTTPCACHE_DIR', 'httpcache')
# HTTPCACHE_EXPIRATION_SECS = 0 # Keep indefinitely
# HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None,
	# Disable compression middleware, so the actual HTML pages are cached
}

HTTPCACHE_ENABLED = False
SPIDER_MODULES = ['hhgregg.spiders']
NEWSPIDER_MODULE = 'hhgregg.spiders'
# DUPEFILTER_DEBUG = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hhgregg (+http://www.yourdomain.com)'
from datetime import datetime
datetime.now().strftime("%Y%m%d_%H%M%S")

FEED_FORMAT = 'csv'
FEED_URI = "%(name)s_%(time)s.csv"

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36'
}

FEED_FORMAT = 'jsonlines'
FEED_URI = "%(name)s_%(time)s.json"

CONCURRENT_REQUESTS=5
RETRY_ENABLED = True