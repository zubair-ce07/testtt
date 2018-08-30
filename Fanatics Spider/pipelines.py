import json
import logging

import pymysql

from Spider.Fanatics import settings


class FanaticsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        table_name = settings.MYSQL_TABLE
        try:
            self.cursor.execute(
                "insert into {} (product_id, breadcrumb, title, brand, categories, "
                "description, details, gender, product_url, image_urls, price, "
                "currency, language, skus)"
                "value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "on duplicate key update product_id=(product_id)".format(table_name),
                (
                    item['product_id'],
                    json.dumps(item['breadcrumb']),
                    item['title'],
                    item['brand'],
                    json.dumps(item['categories']),
                    item['description'],
                    json.dumps(item['details']),
                    item['gender'],
                    item['product_url'],
                    json.dumps(item['image_urls']),
                    item['price'],
                    item['currency'],
                    item['language'],
                    json.dumps(item['skus'])
                ))
            self.connect.commit()

        except Exception as error:
            logging.error(error)
        logging.info('Product added with id: '.format(item['product_id']))
        return item

    def close_spider(self, spider):
        self.connect.close()
