# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class SetItemPrice(object):
    def process_item(self, item, spider):
        item['skus'] = [dict(sku, id=id) for (id, sku) in item['skus'].items()]
        item['price'] = min([x['price'] for x in item['skus']])
        item['currency'] = item['skus'][0]['currency']
        return item
