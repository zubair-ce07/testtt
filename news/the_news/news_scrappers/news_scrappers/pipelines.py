# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from datetime import datetime
from scrapy.exceptions import DropItem
from the_news.models import News, NewsPaper
from django.db import DatabaseError


class NewsScrappersPipeline(object):
    news_paper = None

    def open_spider(self, spider):
        self.news_paper, created = NewsPaper.objects.update_or_create(name='The News',
                                                                      defaults={'name': 'The News',
                                                                                'website': 'https://www.thenews.com.pk/'})

    def process_item(self, item, spider):
        for i in xrange(len(item['url'])):

            try:
                url, date, img_url, title, abstract, detail = self.__clean_news_data(
                    item)

                try:
                    news_item, created = News.objects.update_or_create(news_url=url,
                                                                       defaults={'title': title.encode('utf-8'),
                                                                                 'date': date,
                                                                                 'abstract': abstract.encode('utf-8'),
                                                                                 'news_url': url, 'image_url': img_url,
                                                                                 'detail': detail.encode('utf-8'),
                                                                                 'news_paper': self.news_paper})
                    news_item.save()
                except DatabaseError:
                    raise DropItem("Not inserted in database " % item)
            except Exception as e:
                logging.warning(e.message)
                raise DropItem("Unexpected Values in " % item)
        return item

    def __clean_news_data(self, item):
        date = item['date'][0].strip().strip(
            '\r').replace(" ", "-").replace(",", "")
        date = datetime.strptime(date, '%B-%d-%Y')
        url = item['url'][0].strip()
        img_url = item['img_url'][0].strip()
        abstract = item['abstract'][0].strip()
        title = item['title'][0].strip()
        detail = item['detail'][0]
        return url, date, img_url, title, abstract, detail
