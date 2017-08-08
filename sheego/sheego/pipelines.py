# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem


class SheegoPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['retailer_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['retailer_id'])
            return item
