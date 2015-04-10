# -*- coding: utf-8 -*-

# Scrapy settings for documents_download project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'documents_download'

SPIDER_MODULES = ['documents_download.spiders']
NEWSPIDER_MODULE = 'documents_download.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'documents_download (+http://www.yourdomain.com)'
FILES_STORE = 'D:/downloads'
ITEM_PIPELINES = [
    'documents_download.pipelines.DocumentsDownloadPipeline',
]
DOWNLOAD_DELAY= 5
DOWNLOAD_TIMEOUT = 300