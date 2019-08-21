# -*- coding: utf-8 -*-

import scrapy


class PakwheelsItem(scrapy.Item):
    # define the fields for your item here like:
    make = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    millage = scrapy.Field()
    transmission = scrapy.Field()
    engine_type = scrapy.Field()
    reg_city = scrapy.Field()
    assembly = scrapy.Field()
    engine_capacity = scrapy.Field()
    body_type = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
