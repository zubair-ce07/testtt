BOT_NAME = 'lindex'

SPIDER_MODULES = ['lindex.spiders']
NEWSPIDER_MODULE = 'lindex.spiders'
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'lindex.pipelines.LindexPipeline': 300,
}
