# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class WoolrichPipeline(object):
    def process_item(self, item, spider):
        prices = []
        previous_prices = []
        for key, value in item['skus'].items():
            prices.append(value['price'])
            previous_prices.append((value['previous_price']))
        item['price'] = min(prices)
        previous_price = min(previous_prices)
        if previous_price:
            item['previous_price'] = min(previous_prices)
        if previous_price and item['price'] > previous_price:
            raise DropItem("Sale price is greater than orignal price %s" % item)
        else:
            return item
