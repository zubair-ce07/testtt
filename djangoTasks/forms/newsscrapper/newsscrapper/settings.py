import sys
import os
import django


BOT_NAME = 'newsscrapper'

SPIDER_MODULES = ['newsscrapper.spiders']
NEWSPIDER_MODULE = 'newsscrapper.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

sys.path.append('/home/mubtada/Documents/training_projects/django_training/forms')
os.environ['DJANGO_SETTINGS_MODULE'] = 'forms.settings'

django.setup()

ITEM_PIPELINES = {
    'newsscrapper.pipelines.NewsscrapperPipeline': 300,
}
