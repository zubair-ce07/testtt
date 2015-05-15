# -*- coding: utf-8 -*-

# Scrapy settings for documents_download project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'documents_download'
HTTPCACHE_ENABLED = True
SPIDER_MODULES = ['documents_download.spiders']
NEWSPIDER_MODULE = 'documents_download.spiders'

# from datetime import datetime
# LOG_FILE = "scrapy_%s.log" % datetime.now().strftime("%Y%m%d_%H%M%S")

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'documents_download (+http://www.yourdomain.com)'
FILES_STORE = 'E:/downloads'
ITEM_PIPELINES = [
    'documents_download.pipelines.DocumentsDownloadPipeline',
]
DOWNLOAD_DELAY= 2
DOWNLOAD_TIMEOUT = 500