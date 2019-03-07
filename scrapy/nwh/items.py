# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoctorItem(scrapy.Item):
    full_name = scrapy.Field()
    specialty = scrapy.Field()
    image_url = scrapy.Field()
    source_url = scrapy.Field()
    graduate_education = scrapy.Field()
    crawled_date = scrapy.Field(serializer=str)
    medical_school = scrapy.Field()
    affiliation = scrapy.Field()
    address = scrapy.Field()


class AddressItem(scrapy.Item):
    phone = scrapy.Field()
    fax = scrapy.Field()
    other = scrapy.Field()
