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


class SizeSpiderItem(scrapy.Item):

    # define the fields for your item here like:
    spider_name = scrapy.Field()
    retailer = scrapy.Field()
    currency = scrapy.Field(
        output_processor=Compose(lambda v: re.findall('title="\w*"', v[0])[0].split('=')[-1]),
    )
    market = scrapy.Field()
    category = scrapy.Field()
    retailer_sku = scrapy.Field()
    price = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\D', '', v, flags=re.UNICODE)),
    )
    description = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: replace_escape_chars(v, replace_by=u' ')),
    )
    brand = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: v.split(u'\xa0')[0]),
    )
    image_urls = scrapy.Field()
    trail = scrapy.Field()
    skus = scrapy.Field()
    care = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: replace_escape_chars(v, replace_by=u' '))
    )
    name = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\xa0', u' ', v, flags=re.UNICODE)),
    )
    url = scrapy.Field()
    gender = scrapy.Field()


class SkuItem(scrapy.Item):

    currency = scrapy.Field(
        output_processor=Compose(lambda v: re.findall('title="\w*"', v[0])[0].split('=')[-1]),
    )
    price = scrapy.Field(
        output_processor=MapCompose(unicode.strip, lambda v: re.sub(ur'\D', '', v, flags=re.UNICODE)),
    )
    color = scrapy.Field(
        output_processor=MapCompose(unicode.strip),
    )
    size = scrapy.Field()
    out_of_stock = scrapy.Field(
        output_processor=MapCompose(lambda v: True if v != 'in stock' else False),
    )
