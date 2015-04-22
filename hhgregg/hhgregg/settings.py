# -*- coding: utf-8 -*-

# Scrapy settings for hhgregg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hhgregg'
DOWNLOAD_DELAY = 10


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