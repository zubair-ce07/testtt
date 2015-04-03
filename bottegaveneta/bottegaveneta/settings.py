# -*- coding: utf-8 -*-

# Scrapy settings for bottegaveneta project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bottegaveneta'

SPIDER_MODULES = ['bottegaveneta.spiders']
NEWSPIDER_MODULE = 'bottegaveneta.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bottegaveneta (+http://www.yourdomain.com)'
from datetime import datetime
# LOG_FILE = "scrapy_%s.log" % datetime.now().strftime("%Y%m%d_%H%M%S")

datetime.now().strftime("%Y%m%d_%H%M%S")

FEED_FORMAT = 'csv'
FEED_URI = "%(name)s_%(time)s.csv"

FEED_FORMAT = 'jsonlines'
FEED_URI = "%(name)s_%(time)s.json"