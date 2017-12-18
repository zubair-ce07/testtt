BOT_NAME = 'amazon_scrapper'

SPIDER_MODULES = ['amazon_scrapper.spiders']
NEWSPIDER_MODULE = 'amazon_scrapper.spiders'

ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 6


ITEM_PIPELINES = {
    'amazon_scrapper.pipelines.JsonWriterPipeline': 600,
    'amazon_scrapper.pipelines.DuplicatesPipeline': 300,
}
