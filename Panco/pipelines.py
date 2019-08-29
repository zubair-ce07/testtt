# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from operator import attrgetter

class SetItemPrice(object):
    def process_item(self, item, spider):
        item['skus'] = [dict(sku, id=id) for (id, sku) in item['skus'].items()]
        item['price'] = min([x['price'] for x in item['skus']])
        item['currency'] = item['skus'][0]['currency']
        return item
