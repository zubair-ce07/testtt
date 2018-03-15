# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem


class ProductPipeline(object):

    def __init__(self):
        """
        Declare ids_seen var to avoid duplicate ids
        """
        self.ids_seen = set()

    def open_spider(self, spider):
        """
        Declare category_to_export var, json file names will use this field
        """
        self.category_to_export = {}

    def close_spider(self, spider):
        for exporter in self.category_to_export.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        """
        Create exporter using product category as file name
        """
        category = item['product_cat']
        if category not in self.category_to_export:
            # Create individual files based on combination of gender, category and sub category
            j_file = open(category + '.json', 'w')
            exporter = JsonItemExporter(j_file)
            # Define the fields to export in file
            exporter.fields_to_export = [
                'gender',
                'category',
                'sub_category',
                'brand',
                'name',
                'product_id',
                'product_url',
                'data_id',
                'price',
                'currency',
                'item_info',
                'images',
                'image_urls'
            ]
            exporter.start_exporting()
            self.category_to_export[category] = exporter
        return self.category_to_export[category]

    def process_item(self, item, spider):
        """
        Perform check on different items
        """
        exporter = self._exporter_for_item(item)
        # Check duplication of product ID
        if item['product_id'] in self.ids_seen:
            raise DropItem("Duplicate product found: %s" % item)
        else:
            self.ids_seen.add(item['product_id'])
        # Show message if item info like colors etc. is not available
        if not item["item_info"]:
            item["item_info"] = "Item Information not available"
        # If brand field is empty use "converse" as brand name
        if not item["brand"]:
            item["brand"] = "Converse"
        exporter.export_item(item)
        return item
