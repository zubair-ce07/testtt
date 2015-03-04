# -*- coding: utf-8 -*-

# Scrapy settings for gymboree project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gymboree'

SPIDER_MODULES = ['gymboree.spiders']
NEWSPIDER_MODULE = 'gymboree.spiders'
DOWNLOAD_DELAY = 10
DOWNLOAD_TIMEOUT = 360

from datetime import datetime
# LOG_FILE = "scrapy_%s.log" % datetime.now().strftime("%Y%m%d_%H%M%S")

datetime.now().strftime("%Y%m%d_%H%M%S")

FEED_FORMAT = 'csv'
FEED_URI = "%(name)s_%(time)s.csv"

FEED_FORMAT = 'jsonlines'
FEED_URI = "%(name)s_%(time)s.json"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gymboree (+http://www.yourdomain.com)'
