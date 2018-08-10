# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class WoolrichPipeline(object):

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres' # your password
        database = 'postgres'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into woolrich_content(name,color,price,size,style,path,image,features,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['name'], item['color'], item['price'], item['size'], item['style'], item['path'], item['image'], item['features'], item['description']))
        self.connection.commit()
        return item
