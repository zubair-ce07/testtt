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
