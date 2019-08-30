# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


class CapucPipeline(object):
    @staticmethod
    def process_item(item, spider):
        print("////////////////////////YIELDING_NOW/////////////////////")
        file_name = "ca-{}.json".format(item["state_id"].lower())
        with open(file_name, 'w') as json_file:
            json.dump(item, json_file)
        return item
