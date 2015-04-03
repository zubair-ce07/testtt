# -*- coding: utf-8 -*-

# Scrapy settings for witt_weiden project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'witt_weiden'

SPIDER_MODULES = ['witt_weiden.spiders']
NEWSPIDER_MODULE = 'witt_weiden.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'witt_weiden (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0
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
#DEFAULT_IMAGES_URLS_FIELD = 'image_urls'
#ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
#IMAGES_STORE = 'e:/images'