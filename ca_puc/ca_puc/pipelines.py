# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo


class CaPucPipeline(object):
    def process_item(self, item, spider):
        del item['total_filing_count']
        del item['filing_count']
        return item


class MongoPipeline(object):
    collecction_name = 'proceedings'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # getting configurations from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # openinig db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # handling the proceeding
        self.db[self.collecction_name].insert(dict(item))
        logging.debug('Proceeding:'+item["state_id"]+'added to MongoDB')
        return item
