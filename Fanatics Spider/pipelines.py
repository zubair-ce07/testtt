import datetime
import json
import logging

import pymysql

from Fanatics import settings


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
        sql_query = 'insert into {} (product_id, created_at, breadcrumb, title, brand, categories, ' \
                    'description, details, gender, product_url, image_urls, price, ' \
                    'currency, language, skus)' \
                    'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
                    'on duplicate key update product_id=(product_id)'

        values = (
            item['product_id'], datetime.datetime.now(),
            json.dumps(item['breadcrumb']), item['title'],
            item['brand'], json.dumps(item['categories']),
            item['description'], json.dumps(item['details']),
            item['gender'], item['product_url'],
            json.dumps(item['image_urls']), item['price'],
            item['currency'], item['language'],
            json.dumps(item['skus'])
        )

        try:
            self.cursor.execute(sql_query.format(table_name), values)
            self.connect.commit()

        except Exception as error:
            logging.error(error)
        logging.info('Product added with id: {}'.format(item['product_id']))
        return item

    def close_spider(self, spider):
        self.connect.close()
