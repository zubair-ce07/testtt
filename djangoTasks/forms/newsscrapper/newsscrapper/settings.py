import sys
import os
import django


BOT_NAME = 'newsscrapper'

SPIDER_MODULES = ['newsscrapper.spiders']
NEWSPIDER_MODULE = 'newsscrapper.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'forms.settings'

django.setup()

ITEM_PIPELINES = {
    'newsscrapper.pipelines.NewsscrapperPipeline': 300,
}
