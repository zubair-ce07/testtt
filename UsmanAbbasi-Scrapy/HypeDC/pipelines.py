# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
con = None


class HypedcPipeline(object):
    def process_item(self, item, spider):
        images_list = self.image_urls_formatting(item)
        self.store_in_db(item, images_list)
        return item

    def image_urls_formatting(self, item):
        images_list = ""
        for url in item['image_urls']:
            images_list = images_list + " " + url
        return images_list

    def __init__(self):
        self.setup_db_con()
        self.drop_hype_table()
        self.create_hype_table()

    def setup_db_con(self):
        self.con = sqlite3.connect('./test.db')
        self.cur = self.con.cursor()

    def drop_hype_table(self):
        self.cur.execute("DROP TABLE IF EXISTS HYPE")

    def close_db(self):
        self.con.close()

    def __del__(self):
        self.close_db()

    def create_hype_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS HYPE(item_id TEXT PRIMARY KEY NOT NULL, \
        url TEXT, \
        name TEXT, \
        brand TEXT, \
        description TEXT, \
        currency TEXT, \
        is_discounted BOOLEAN, \
        price REAL, \
        old_price REAL, \
        color_name TEXT, \
        image_list TEXT \
        )")

    def store_in_db(self, item, images_list):
        self.cur.execute("INSERT INTO HYPE(\
            item_id, \
            url, \
            name, \
            brand, \
            description, \
            currency, \
            is_discounted, \
            price, \
            old_price, \
            color_name, \
            image_list \
            ) \
        VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            item['item_id'],
            item['url'],
            item['name'],
            item['brand'],
            item['description'],
            item['currency'],
            item['is_discounted'],
            item['price'],
            item['old_price'],
            item['color_name'],
            images_list
        ))
        self.con.commit()
