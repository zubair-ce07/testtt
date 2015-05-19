# -*- coding: utf-8 -*-

# Scrapy settings for stores_location_spiders project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stores_location_spiders'

SPIDER_MODULES = ['stores_location_spiders.spiders']
NEWSPIDER_MODULE = 'stores_location_spiders.spiders'

FEED_FORMAT = 'jsonlines'
FEED_URI = "jsons/%(name)s-%(time)s.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stores_location_spiders (+http://www.yourdomain.com)'
from datetime import datetime
datetime.now().strftime("%Y%m%d_%H%M%S")
HTTPCACHE_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36'
}

# DOWNLOAD_DELAY = 5
# CONCURRENT_REQUESTS=5