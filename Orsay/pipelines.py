# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
from scrapy.exceptions import DropItem


class FilterDuplicate(object):

    def __init__(self):
        self.pid = set()
    
    def process_item(self, item, spider):
        if item['retailer_sku'] in self.pid:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.pid.add(item['retailer_sku'])
            return item

class ValidateItem(object):

    def process_item(self, item, spider):
        item['description'] = [desc.strip().strip('-').strip() for desc in item['description']][2:]
        item['image_urls'] = [re.findall(r'.*.jpg' , img_url)[0] for img_url in item['image_urls']]
        return item

class JsonWriteItemPipeline(object):
    
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item