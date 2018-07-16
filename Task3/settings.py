BOT_NAME = 'Task3'

SPIDER_MODULES = ['Task3.spiders']
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 0.25

ITEM_PIPELINES = {
    'Task3.pipelines.DuplicatesRemovalPipeline': 100,
}

FEED_FORMAT = 'json'
FEED_URI = 'output/productsdetail.json'


