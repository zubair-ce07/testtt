# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DawnScraperItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    image_url = scrapy.Field()
    pub_date = scrapy.Field()
    publisher = scrapy.Field()
    url = scrapy.Field()
