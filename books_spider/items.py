# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader


class BooksSpiderItem(scrapy.Item):
    Book_Name = scrapy.Field()
    Book_price = scrapy.Field()
    Book_Category = scrapy.Field()
    Book_Author = scrapy.Field()
    Book_Condition = scrapy.Field()
    Book_Language = scrapy.Field()
    Book_Weight = scrapy.Field()
    Image__Img_Url = scrapy.Field()


class BookItemLoader(ItemLoader):
    speciality_in = MapCompose()
