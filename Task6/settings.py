BOT_NAME = 'Task6'
SPIDER_MODULES = ['Task6.spiders']
ITEM_PIPELINES = {
    'Task6.pipelines.DuplicatesRemovalPipeline': 100,
}
FEED_FORMAT = 'json'
FEED_URI = 'output/productsdetail.json'
FEED_EXPORT_ENCODING = "utf-8"
