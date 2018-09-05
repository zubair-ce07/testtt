BOT_NAME = 'Fanatics'

SPIDER_MODULES = ['Fanatics.spiders']
NEWSPIDER_MODULE = 'Fanatics.spiders'

ROBOTSTXT_OBEY = True

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'FanaticsDB'
MYSQL_TABLE = 'FanaticsItem'

ITEM_PIPELINES = {
    'Fanatics.pipelines.FanaticsPipeline': 300,
}
