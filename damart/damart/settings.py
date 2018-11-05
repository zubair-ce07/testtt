BOT_NAME = 'damart'

SPIDER_MODULES = ['damart.spiders']
NEWSPIDER_MODULE = 'damart.spiders'


USER_AGENT = 'Mozilla/5.0 (Windows; Linux; Android 4.2.1; \
            en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 \
            (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19'

ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'damart.middlewares.DamartDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'damart.pipelines.DamartPipeline': 300,
}
