# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksScraperItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    product_information = scrapy.Field()
