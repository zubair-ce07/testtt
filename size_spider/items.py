# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.utils.markup import replace_escape_chars


def compact(s):
    """ returns None if string is empty, otherwise string itself """
    return s if s else None


class SizeSpiderItem(scrapy.Item):

    # define the fields for your item here like:
    spider_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer = scrapy.Field(
        output_processor=TakeFirst()
    )
    currency = scrapy.Field(
        output_processor=Compose(lambda v: re.findall('title="\w*"', v[0])[0].split('=')[-1]),
    )
    market = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field()
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst(),
        input_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\D', '', v, flags=re.UNICODE), compact),
    )
    description = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: replace_escape_chars(v, replace_by=u' ')),
    )
    brand = scrapy.Field(
        output_processor=TakeFirst(),
        input_processor=MapCompose(unicode.strip, lambda v: v.split(u'\xa0')[0]),
    )
    image_urls = scrapy.Field()
    trail = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field(
        input_processor=MapCompose(lambda v: replace_escape_chars(v, replace_by=u''),
                                   lambda v: re.sub(ur'-', '', v, flags=re.UNICODE)),
        output_processor=Compose(lambda v: v[2] if len(v) > 3 else u'')
    )
    name = scrapy.Field(
        input_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\xa0', u' ', v, flags=re.UNICODE)),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    gender = scrapy.Field(
        output_processor=TakeFirst()
    )


class SkuItem(scrapy.Item):

    currency = scrapy.Field(
        output_processor=Compose(lambda v: re.findall('title="\w*"', v[0])[0].split('=')[-1]),
    )
    price = scrapy.Field(
        output_processor=TakeFirst(),
        input_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\D', '', v, flags=re.UNICODE), compact),
    )
    color = scrapy.Field(
        input_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'-', '', v, flags=re.UNICODE)),
        output_processor=TakeFirst()
    )
    size = scrapy.Field()
    out_of_stock = scrapy.Field(
        output_processor=MapCompose(lambda v: True if v != 'in stock' else False),
    )



