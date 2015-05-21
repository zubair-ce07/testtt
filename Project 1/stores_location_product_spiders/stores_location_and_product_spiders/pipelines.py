# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoresLocationProductPipeline(object):
    def process_item(self, item, spider):
        for key_name in list(item.keys()):
            self.delete_empty_key(item, key_name)
            if key_name == 'items':
                for all_products in item[key_name]:
                    for sub_key in list(all_products.keys()):
                        self.delete_empty_key(all_products, sub_key)
        return item

    def delete_empty_key(self, item, key):
        if not(item[key]) and isinstance(item[key], bool) == False:
            del item[key]