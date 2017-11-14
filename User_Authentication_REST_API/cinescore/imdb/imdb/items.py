# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    title = scrapy.Field()
    movie_id = scrapy.Field()
    rating = scrapy.Field()
    release_date = scrapy.Field()
    content_rating = scrapy.Field()
    plot = scrapy.Field()
    poster = scrapy.Field()
    url = scrapy.Field()
    categories = scrapy.Field()
    base_url = scrapy.Field()
