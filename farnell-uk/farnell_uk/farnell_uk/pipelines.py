# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CleansingPipeline(object):
    def process_item(self, item, spider):
        keys = list(item.keys())
        for key in keys:
            if not item[key]:
                del item[key]
        return item
