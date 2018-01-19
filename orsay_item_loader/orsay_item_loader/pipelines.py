# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import psycopg2


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))

        self.insert_item()
        self.insert_items()
        self.search_item('12345')
        self.search_items('12345')
        self.update_item('6789')
        self.update_items('Leather Jacket')
        self.delete_item('12345')
        self.delete_items('Leather Jacket')
        self.delete_all_items()
        self.drop_collection()

        return item

    def insert_item(self):
        temp_item = {
            'product_id': '12345',
            'name': 'Leather Jacket',
            'price': '300',
            'currency': 'USD',
            'sku': {'black_XL': {
                            'color': 'black',
                            'size': 'XL'
                        }
                    },
            'lang': 'en',
        }
        result = self.db[self.collection_name].insert_one(dict(temp_item))
        print ("Inserted item object ID: {}".format(result.inserted_id))

    def insert_items(self):
        temp_item1 = {
            'product_id': '12345',
            'name': 'Leather Jacket',
            'price': '300',
            'currency': 'USD',
            'sku': {'black_XL': {
                            'color': 'black',
                            'size': 'XL'
                            }
                    },
            'lang': 'en',
        }
        temp_item2 = {
            'product_id': '6789',
            'name': 'Denim Jeans',
            'price': '100',
            'currency': 'USD',
            'sku': {'blue_XL': {
                        'color': 'blue',
                        'size': 'XL'
                        }
                    },
            'lang': 'en',
        }

        result = self.db[self.collection_name].insert_many([temp_item1, temp_item2])
        print ("Inserted items object ID's: {}".format(result.inserted_ids))

    def search_item(self, product_id):
        searched_item = self.db[self.collection_name].find_one({'product_id' : product_id})
        print ("Searched item: {}".format(searched_item))

    def search_items(self, product_id):
        cursor = self.db[self.collection_name].find({'product_id' : product_id})
        for document in cursor:
            print(document)

    def update_item(self, product_id):
        result = self.db[self.collection_name].update_one(
            {"product_id": product_id},
            {
                "$set": {
                    "price": "99.99"
                }
            }
        )
        print ("Number of item(s) matched: {}".format(result.matched_count))
        print ("Number of item(s) modified: {}".format(result.modified_count))

    def update_items(self, product_name):
        result = self.db[self.collection_name].update_many(
            {"name": product_name},
            {
                "$set": {
                    "price": "199.99"
                }
            }
        )
        print ("Number of item(s) matched: {}".format(result.matched_count))
        print ("Number of item(s) modified: {}".format(result.modified_count))

    def delete_item(self, product_id):
        result = self.db[self.collection_name].delete_one({'product_id' : product_id})
        print ("Number of item(s) deleted: {}".format(result.deleted_count))

    def delete_items(self, product_name):
        result = self.db[self.collection_name].delete_many({"name": product_name})
        print ("Number of item(s) deleted: {}".format(result.deleted_count))

    def delete_all_items(self):
        result = self.db[self.collection_name].delete_many({})
        print ("Number of item(s) deleted: {}".format(result.deleted_count))

    def drop_collection(self):
        self.db[self.collection_name].drop()


class PostgresPipeline(object):

    def __init__(self, conn_string):
        self.POSTGRES_CONNECTION_STRING = conn_string

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            conn_string=crawler.settings.get('POSTGRES_CONNECTION_STRING'),
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(self.POSTGRES_CONNECTION_STRING)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()

            self.create_table(cursor)
            self.insert_item(cursor,item)
            self.update_item(cursor, item)
            self.display_items(cursor)
            self.delete_item(cursor, item)

        except Exception as e:
            print(e)

        return item

    def create_table(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS items( 
                                       product_id bigint, 
                                       name varchar(50),
                                       price FLOAT,
                                       brand varchar(50),
                                       currency varchar(3),
                                       images varchar(500)                             
                                   );""")
        self.conn.commit()

    def insert_item(self, cursor, item):
        cursor.execute("""INSERT INTO items VALUES(%s, %s, %s, %s, %s, %s)""", (
                                item['retailer_sk'],
                                item['name'],
                                item['price'],
                                item['brand'],
                                item['currency'],
                                item['image_urls'],
                        ))
        self.conn.commit()

    def update_item(self, cursor, item):
        cursor.execute("""UPDATE items SET 
                          name = %s,
                          price = %s
                          WHERE
                          product_id = %s""",
                        ('Wool Sweater', 15.75, item['retailer_sk'],))
        self.conn.commit()

    def delete_item(self, cursor, item):
        cursor.execute("""DELETE FROM items 
                          WHERE
                          product_id = %s""",
                       (item['retailer_sk'],))
        self.conn.commit()

    def display_items(self, cursor):
        cursor.execute("""SELECT * FROM items""")
        rows = cursor.fetchall()
        print(rows)