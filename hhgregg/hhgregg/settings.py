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

HTTPCACHE_IGNORE_HTTP_CODES = range(500,599)
HTTPCACHE_DIR = os.environ.get('HTTPCACHE_DIR', 'httpcache')
HTTPCACHE_EXPIRATION_SECS = 0 # Keep indefinitely
HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None,
	# Disable compression middleware, so the actual HTML pages are cached
}

HTTPCACHE_ENABLED = True
SPIDER_MODULES = ['hhgregg.spiders']
NEWSPIDER_MODULE = 'hhgregg.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hhgregg (+http://www.yourdomain.com)'
from datetime import datetime
datetime.now().strftime("%Y%m%d_%H%M%S")

FEED_FORMAT = 'csv'
FEED_URI = "%(name)s_%(time)s.csv"

FEED_FORMAT = 'jsonlines'
FEED_URI = "%(name)s_%(time)s.json"