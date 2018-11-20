# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

def _clean_in(self, values):
    return [value.strip("\n ") if type(value) == str else value for value in values]

def _option(self, values):
    for value in values:
        if "yes" in value.lower():
            return ["y"]
        elif "no" in value.lower():
            return ["n"]
        
class CompareItem(scrapy.Item):
    source = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()
    effective_from = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    supply = scrapy.Field()
    peak_rate = scrapy.Field() #
    shoulder = scrapy.Field()#
    off_peak_rate = scrapy.Field() #
    green = scrapy.Field()
    green_note = scrapy.Field()
    etf = scrapy.Field()
    contract_length = scrapy.Field()
    meter_type = scrapy.Field()
    solar = scrapy.Field()


class CompareItemLoader(ItemLoader):
    default_item_class = CompareItem
    default_output_processor = TakeFirst()
    default_input_processor = _clean_in

    # green_in = _option