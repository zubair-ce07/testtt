BOT_NAME = 'Task5'
SPIDER_MODULES = ['Task5.spiders']
ITEM_PIPELINES = {
    'Task5.pipelines.DuplicatesRemovalPipeline': 100,
}
