BOT_NAME = 'Task3'
SPIDER_MODULES = ['Task3.spiders']
ITEM_PIPELINES = {'Task3.pipelines.DuplicatesRemovalPipeline': 100}
FEED_FORMAT ='json'
FEED_URI ='output/productsdetail.json'
FEED_EXPORT_ENCODING = "utf-8"
