# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonItem(scrapy.Item):
    pokemon = scrapy.Field()
    moves = scrapy.Field()
    counters = scrapy.Field()
    cp_chart = scrapy.Field()
    iv_chart = scrapy.Field()
    hp_chart = scrapy.Field()
    image_urls = scrapy.Field()
    pass
