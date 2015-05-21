# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoresLocationProductPipeline(object):
    def process_item(self, item, spider):
        for key_name in list(item.keys()):
            if not(item[key_name]):
                del item[key_name]
        return item
