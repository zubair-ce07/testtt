# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import os


class JsonWriterPipeline(object):
    def __init__(self):
        self.dir_path = '../witt-weiden-data'
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def process_item(self, item, spider):
        with open(os.path.join(self.dir_path, item['retailer_sku'] +
                '.json'), 'w') as jsonfile:
            jsonfile.write(json.dumps(dict(item), indent=3, sort_keys=True))
        return item
