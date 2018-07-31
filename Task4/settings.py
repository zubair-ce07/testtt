BOT_NAME = 'Task4'
SPIDER_MODULES = ['Task4.spiders']
ITEM_PIPELINES = {
    'Task4.pipelines.DuplicatesRemovalPipeline': 100,
}
FEED_FORMAT = 'json'
FEED_URI = 'output/productsdetail.json'
FEED_EXPORT_ENCODING = "utf-8"