BOT_NAME = 'Task3'
SPIDER_MODULES = ['Task3.spiders']
ITEM_PIPELINES = {'Task3.pipelines.DuplicatesRemovalPipeline': 100}
