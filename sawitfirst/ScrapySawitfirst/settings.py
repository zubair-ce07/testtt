BOT_NAME = 'ScrapySawitfirst'

SPIDER_MODULES = ['ScrapySawitfirst.spiders']
NEWSPIDER_MODULE = 'ScrapySawitfirst.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.25

ITEM_PIPELINES = {
    'ScrapySawitfirst.pipelines.DuplicatesPipeline': 0,
}

DEFAULT_REQUEST_HEADERS = {
    'referer': 'https://www.isawitfirst.com'
}
