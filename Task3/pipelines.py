# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from operator import attrgetter

class RequiredProductFields(object):
    required_fields = ['name', 'retailer_sku', 'lang', 'category', 'brand', 'url',
                       'description', 'care', 'image_urls', 'skus']

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem(f"Missing field: {field} in {item}")
        return item

class SetItemPrice(object):
    def process_item(self, item, spider):
        skus = []
        item_sku = item['skus']
        for id in item_sku:
            sku = item_sku[id]
            sku['id'] = id
            skus.append(sku)
        item['skus'] = skus
        item['price'] = min([x['price'] for x in skus])
        item['currency'] = skus[0]['currency']
        return item

