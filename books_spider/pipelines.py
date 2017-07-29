# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from books_spider.run_project import BooksTable, db_connect, create_books_table


class BooksSpiderPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates books table.
        """
        engine = db_connect()
        create_books_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        book = BooksTable(**item)

        try:
            session.add(book)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

