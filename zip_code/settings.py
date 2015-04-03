# -*- coding: utf-8 -*-

# Scrapy settings for zip_code project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zip_code'

SPIDER_MODULES = ['zip_code.spiders']
NEWSPIDER_MODULE = 'zip_code.spiders'
DOWNLOAD_DELAY = 10

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zip_code (+http://www.yourdomain.com)'
