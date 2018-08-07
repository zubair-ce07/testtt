BOT_NAME = 'Task4'
SPIDER_MODULES = ['Task4.spiders']
ITEM_PIPELINES = {
    'Task4.pipelines.DuplicatesRemovalPipeline': 100,
}
