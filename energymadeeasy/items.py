# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EnergymadeeasyItem(scrapy.Item):
    source = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()
    effective_from = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    supply = scrapy.Field()
    peak_rate = scrapy.Field()
    shoulder = scrapy.Field()
    off_peak_rate = scrapy.Field()
    green = scrapy.Field()
    green_note = scrapy.Field()
    etf = scrapy.Field()
    contract_length = scrapy.Field()
    meter_type = scrapy.Field()
    solar = scrapy.Field()
    solar_meter_fee = scrapy.Field()
    guaranteed_discount_off_usage = scrapy.Field()
