# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LululemonPipeline(object):
    def process_item(self, item, spider):
        self.store_in_db(item)
        return item

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
        is_discounted BOOLEAN, \
        price REAL, \
        old_price REAL, \
        color_name TEXT, \
        image_list TEXT \
        )")

    def store_in_db(self, item):
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