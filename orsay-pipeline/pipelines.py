# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter

class OrsayPipeline(object):
    def process_item(self, item, spider):
        return item


class CategoryFilterPipeline(object):
    def open_spider(self, spider):
        self.file_names = {}

    def close_spider(self, spider):
        total_item = 0
        for value in self.file_names.values():
            value['file'].finish_exporting()
            print('File Name: {}  Item Count: {}'.format(value['file_name'], value['item_count']))
            total_item += value['item_count']
        print('Total Items: {}'.format(total_item))

    def process_item(self, item, spider):
        category = item['category']
        category = '_'.join(category)
        if category not in self.file_names.keys():
            self.file_names.update({
                category: {
                    'file': JsonItemExporter(open('./items/{}.json'.format(category), 'wb+')),
                    'file_name': './items/{}.json'.format(category),
                    'item_count': 0
                }
            })
            self.file_names[category]['file'].start_exporting()
        exporter = self.file_names[category]['file']
        exporter.export_item(item)
        self.file_names[category]['item_count'] += 1
        return item

