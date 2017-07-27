# -*- coding: utf-8 -*-

import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite


class WebSpiderProjectPipeline(object):
    def __init__(self):
        self.dbconnect()
        self.createtable()

    def __del__(self):
        self.closeDB()

    def dbconnect(self):
        self.con = lite.connect('/home/hamza/test.db')  # Change this to your own directory
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
            Item_Id INT, \
            Url TEXT, \
            Name TEXT, \
            Brand TEXT, \
            Description TEXT, \
            Currency TEXT, \
            Is_Discounted BOOLEAN, \
            Price REAL, \
            Old_Price TEXT, \
            Color_Name TEXT, \
            Image_Urls TEXT \
            )")

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def storeInDb(self, item):
        self.cur.execute("INSERT INTO Products(\
            Item_Id, \
            Url, \
            Name, \
            Brand, \
            Description, \
            Currency, \
            Is_Discounted, \
            Price, \
            Old_Price, \
            Color_Name, \
            Image_Urls \
            )\
             VALUES (?,?,?,?,?,?,?,?,?,?,?)", \
            ( \
                    int(item.get('item_id', 0)),
                    item.get('url', ''),
                    item.get('name', ''),
                    item.get('brand', ''),
                    item.get('description', ''),
                    item.get('currency', ''),
                    item.get('is_discounted', ''),
                    float(item.get('price', 0.0)),
                    item.get('old_price', ''),
                    item.get('color_name', ''),
                    json.dumps(item.get('image_urls', ''))
            ))
        self.con.commit()

