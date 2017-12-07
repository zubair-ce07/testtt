# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class ValidationPipeline(object):

    def process_item(self, item, spider):
        required_fields = [
            'category',
            'title',
            'product_url',
            'locale',
            'currency',
            'description',
            'product_id',
            'variations'
        ]
        item['description'] = [re.sub('<.*?>', ' ', row) for row in item['description']]
        for field in required_fields:
            if item[field]:
                if field == 'variations':
                    for color in item[field]:
                        if not item[field][color]['code']:
                            del item[field][color]['code']
                        if not item[field][color]['image_urls']:
                            del item[field][color]['image_urls']
                        if not item[field][color]['sizes']:
                            del item[field][color]['sizes']
                    continue
            else:
                del item[field]
        return item
