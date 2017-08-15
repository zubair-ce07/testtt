# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import json
con = None


class LululemonPipeline(object):
    def process_item(self, item, spider):
        sku, image_urls = self.format_readings(item)
        self.store_in_db(item, image_urls, sku)
        return item

    def format_readings(self, item):
        sku = json.dumps(item['sku'])
        image_urls = json.dumps(item['image_urls'])
        return sku, image_urls

    def __init__(self):
        self.setup_db_con()
        self.drop_lemon_table()
        self.create_lemon_table()

    def setup_db_con(self):
        self.con = sqlite3.connect('./test.db')
        self.cur = self.con.cursor()

    def drop_lemon_table(self):
        self.cur.execute("DROP TABLE IF EXISTS LEMON")

    def close_db(self):
        self.con.close()

    def __del__(self):
        self.close_db()

    def create_lemon_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS LEMON(item_id TEXT PRIMARY KEY NOT NULL, \
        url TEXT, \
        name TEXT, \
        brand TEXT, \
        description TEXT, \
        currency TEXT, \
        sku TEXT, \
        image_urls TEXT \
        )")

    def store_in_db(self, item, image_urls, sku):
        self.cur.execute("INSERT INTO LEMON(\
            item_id, \
            url, \
            name, \
            brand, \
            description, \
            currency, \
            sku, \
            image_urls \
            ) \
        VALUES( ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            item['item_id'],
            item['url'],
            item['name'],
            item['brand'],
            item['description'],
            item['currency'],
            sku,
            image_urls
        ))
        self.con.commit()