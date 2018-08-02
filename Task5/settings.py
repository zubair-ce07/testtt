BOT_NAME = 'Task5'
SPIDER_MODULES = ['Task5.spiders']
ITEM_PIPELINES = {
    'Task5.pipelines.DuplicatesRemovalPipeline': 100,
}
FEED_FORMAT = 'json'
FEED_URI = 'output/productsdetail.json'
FEED_EXPORT_ENCODING = "utf-8"
