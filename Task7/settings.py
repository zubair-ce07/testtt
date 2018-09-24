BOT_NAME = 'Task7'
SPIDER_MODULES = ['Task7.spiders']
ITEM_PIPELINES = {
    'Task7.pipelines.DuplicatesRemovalPipeline': 100,
}
