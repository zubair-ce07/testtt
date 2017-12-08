# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ValidationPipeline(object):

    def process_item(self, item, spider):
        required_fields = list(item.keys())
        for field in required_fields:
            if item[field]:
                if field == 'variations':
                    for color in item[field]:
                        variation_item_keys = list(item[field][color].keys())
                        for key in variation_item_keys:
                            if not item[field][color][key]:
                                del item[field][color][key]
                continue
            else:
                del item[field]
        return item
