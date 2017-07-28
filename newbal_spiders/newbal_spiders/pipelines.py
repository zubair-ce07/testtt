# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sqlite3 as lite

class NewbalSpidersPipeline(object):
    def __init__(self):
        self.dbconnect()
        self.createtable()

    def __del__(self):
        self.closeDB()

    def dbconnect(self):
        self.con = lite.connect('/home/hamza/S')  # Change this to your own directory
        self.cur = self.con.cursor()

    def createtable(self):
        self.dropProductsTable()
        self.createProductsTable()

    def dropProductsTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Products")

    def closeDB(self):
        self.con.close()

    def createProductsTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Products(id INTEGER PRIMARY KEY NOT NULL, \
            ProductUrl TEXT, \
            ProductId TEXT, \
            Title TEXT, \
            Category TEXT, \
            Description TEXT, \
            Locale TEXT, \
            Currency TEXT, \
            VariationItems TEXT, \
            SizeItems TEXT \
            )")

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self, item):
        self.cur.execute("INSERT INTO Products(\
            ProductUrl, \
            ProductId, \
            Title, \
            Category, \
            Description, \
            Locale, \
            Currency, \
            VariationItems, \
            SizeItems \
            )\
             VALUES (?,?,?,?,?,?,?,?,?)", \
                         ( \
                             item.get('product_url', ''),
                             item.get('product_id', ''),
                             item.get('title', ''),
                             item.get('category', ''),
                             item.get('description', ''),
                             item.get('locale', ''),
                             item.get('currency', ''),
                             json.dumps(item.get('variationitems', '')),
                             json.dumps(item.get('sizeitems',''))
                         ))
        self.con.commit()
