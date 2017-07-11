# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy.exceptions import DropItem
from the_news.models import News, NewsPaper
from django.db import DatabaseError

class NewsScrappersPipeline(object):
    news_paper = None

    def open_spider(self, spider):
        self.news_paper, created = NewsPaper.objects.update_or_create(name='The News',
                                                                      defaults={'name': 'The News',
                                                                                'source_url': 'https://www.thenews.com.pk/'})

    def process_item(self, item, spider):
        try:
            news_item, created = News.objects.update_or_create(source_url=item['url'],
                                                               defaults={'title': item['title'],
                                                                         'date': item['date'],
                                                                         'abstract': item['abstract'],
                                                                         'source_url': item['url'],
                                                                         'image_url': item['img_url'],
                                                                         'detail': item['detail'].encode('utf-8'),
                                                                         'news_paper': self.news_paper})
            news_item.save()
        except DatabaseError as e:
            logging.warning(e.message)
            raise DropItem("Item Not inserted in database")
        except Exception as e:
            logging.warning(e.message)
            raise DropItem("Unexpected Values in item")
        return item
