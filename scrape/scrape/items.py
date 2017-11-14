# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


class Addressitem(scrapy.Item):
    phone = scrapy.Field()
    fax = scrapy.Field()
    others = scrapy.Field()


class Specialtyitem(scrapy.Item):
    name = scrapy.Field()


class GradstudiesItem(scrapy.Item):
    Type = scrapy.Field()
    name = scrapy.Field()


class Product(scrapy.Item):
    crawled_date = scrapy.Field(serializer=str)
    source_url = scrapy.Field(serializer=str)
    board_of_certifications = scrapy.Field()
    full_name = scrapy.Field()
    medical_school = scrapy.Field()
    image_url = scrapy.Field()
    internship = scrapy.Field()
    fellowship = scrapy.Field()
    address = scrapy.Field(serializer=Addressitem)
    specialty = scrapy.Field(serializer=Specialtyitem)
    graduate_studies = scrapy.Field(serializer=GradstudiesItem)


class Addressitemloader(ItemLoader):
    default_item_class = Addressitem


class SpecialtyitemLoader(ItemLoader):
    default_item_class = Specialtyitem
    default_input_processor = MapCompose(lambda s: s.split(','))


class GradstudiesItemLoader(ItemLoader):
    default_item_class = GradstudiesItem
    default_output_processor = TakeFirst()


class ProductLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()
