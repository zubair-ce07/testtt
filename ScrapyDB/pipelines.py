# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from ScrapyDB.items import StackItem, VariationItem, SizeItem
from models import Product_Variation, Product, db_connect, create_table, Product_Size


class ChildrenPlacePipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        product_item = StackItem()
        variation_item = VariationItem()
        size_item = SizeItem()
        sizes =[]

        for item_filed in item:
            if item_filed is not 'variations':
                product_item[item_filed]=item[item_filed]
            else:
                for variation_filed in item['variations']:
                    if variation_filed is not 'sizes':
                        variation_item[variation_filed] = item['variations'][variation_filed]
                    else:
                        sizes = item['variations']['sizes']
        product = Product(**product_item)
        product_variation = Product_Variation(**variation_item)
        try:
            session.add(product)
            session.flush()
            product_variation.store_keeping_unit = product.store_keeping_unit
            session.add(product_variation)
            for size in sizes:
                size_item = size
                product_size = Product_Size(**size_item)
                product_size.store_keeping_unit = product.store_keeping_unit
                session.add(product_size)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

