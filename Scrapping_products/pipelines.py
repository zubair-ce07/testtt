# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class ScrapyNavabiPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'navabi-uk-crawl' and item.get('price') < 1000:
            raise DropItem('In {} price is less than 1000'.format(item))
        else:
            return item
