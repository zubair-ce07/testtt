# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime


class ItemPipeline(object):
    def open_spider(self, spider):
        self.crawl_start_time = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')

    def process_item(self, item, spider):
        item['crawl_start_time'] = self.crawl_start_time
        return item
