# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class OrsayPipeline(object):
    """Pipeline for removing duplicates"""

    def __init__(self):
        self.ids = set()

    def process_item(self, item, spider):
        if item['_id'] in self.ids:
            print("Duplicate Found: ", item["_id"])
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids.add(item['_id'])
            return item
