BOT_NAME = 'mashable'

SPIDER_MODULES = ['mashable.spiders']
NEWSPIDER_MODULE = 'mashable.spiders'


ITEM_PIPELINES = {
    'mashable.pipelines.DuplicatesPipeline': 300,
}

SPIDER_MIDDLEWARES = {
    'mashable.middlewares.DateTimeFilterMiddleware': 543,
}
