# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader.processors import TakeFirst, Compose, Join, Identity


class HypedcItem(scrapy.Item):
    item_id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    is_discounted = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    color_name = scrapy.Field()
    image_urls = scrapy.Field()


def get_item_id(url):
    item_id_match = re.search('prod[0-9]*', url[0])
    return item_id_match.group(0)


def get_description(description):
    return description


class LululemonItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    item_id = scrapy.Field(input_processor=Compose(get_item_id),
                           output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=Compose(get_description),
                               output_processor=Join(". "))
    currency = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field(output_processor=TakeFirst())
    skus = scrapy.Field(output_processor=Identity())
