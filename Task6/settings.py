BOT_NAME = 'Task6'
SPIDER_MODULES = ['Task6.spiders']
ITEM_PIPELINES = {
    'Task6.pipelines.DuplicatesRemovalPipeline': 100,
}
