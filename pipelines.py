# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector as mc


class PakwheelsPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mc.connect(user='root', password='1234', host='127.0.0.1')
        self.mycursor = self.conn.cursor()
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS wheelsDB')
        self.mycursor.execute('USE wheelsDB')

    def create_table(self):
        self.mycursor.execute('DROP TABLE IF EXISTS usedCars')
        tbl_des = (
            'CREATE TABLE IF NOT EXISTS usedCars('
            'used_cars_id int AUTO_INCREMENT,'
            'make varchar(15),'
            'model varchar(15),'
            'year varchar(5),'
            'millage varchar(10),'
            'transmission varchar(10),'
            'engine_type varchar(10),'
            'reg_city varchar(10),'
            'assembly varchar(10),'
            'engine_capacity varchar(10),'
            'body_type varchar(10),'
            'features varchar(500),'
            'description varchar(500),'
            'PRIMARY KEY(used_cars_id) )'
        )
        self.mycursor.execute(tbl_des)

    def store_db(self, make, model, year, millage, transmission, eng_type, reg_city, asmb,
                 eng_cap, body_type, features, desc):
        tbl_in_sql = """INSERT INTO usedCars(make, model, year, millage, transmission, engine_type, reg_city,
                assembly, engine_capacity, body_type, features, description)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        features = ''.join(i for i in features)
        features = features.strip()
        tbl_in_val = (make, model, year, millage, transmission, eng_type, reg_city, asmb,
                      eng_cap, body_type, features, desc)
        self.mycursor.execute(tbl_in_sql, tbl_in_val)
        self.conn.commit()

    def process_item(self, items, spider):
        self.store_db(items['make'], items['model'], items['year'], items['millage'], items['transmission'],
                      items['engine_type'], items['reg_city'], items['assembly'], items['engine_capacity'],
                      items['body_type'], items['features'], items['description'])
        return items
