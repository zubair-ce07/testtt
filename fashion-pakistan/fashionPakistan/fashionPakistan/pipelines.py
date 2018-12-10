# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem


class FilterDuplicate(object):
    def __init__(self):
        self.pid = set()

    def process_item(self, item, spider):
        if item['product_sku'] in self.pid:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.pid.add(item['product_sku'])
            return item


class VerifyProduct(object):
    def process_item(self, item, spider):
        if not(item["product_sku"]) or not(item["url"]) or not(item["name"]) or not(item["skus"]):
            raise DropItem("Basic Things are not found: %s" % item)
        
        return item

class JsonWrite(object):
    def open_spider(self, spider):
        self.file = open(spider.name+'.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
