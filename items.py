# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import string
import re
import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def get_gender(gender):

    if gender == u'D':
        return 'women'
    else:
        return 'men'


def filter_numbers(sku):
    sku = str(sku)
    all = string.maketrans('', '')
    nodigs = all.translate(all, string.digits)
    return unicode(sku.translate(all, nodigs))


def get_price(price):
    price = str(price.encode('utf-8'))
    if len(price) < 1:
        return -1
    return int(re.sub('[\xc2\x80,]', '', price).strip())


class ProductItem(Item):
    brand = Field(output_processor=TakeFirst())
    care = Field(input_processor=MapCompose(unicode.strip))
    category = Field()
    description = Field(input_processor=MapCompose(unicode.strip))
    gender = Field(input_processor=MapCompose(TakeFirst(), get_gender), output_processor=TakeFirst())
    image_urls = Field(input_processor=MapCompose(unicode.strip))
    lang = Field(output_processor=TakeFirst())
    market = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    retailer = Field(output_processor=TakeFirst())
    retailer_sku = Field(input_processor=MapCompose(unicode.strip, filter_numbers), output_processor=TakeFirst())
    skus = Field(output_processor=TakeFirst())


class SkuItemDetail(Item):
    colour = Field(output_processor=TakeFirst())
    currency = Field(output_processor=TakeFirst())
    previous_prices = Field(input_processor=Compose(TakeFirst(), get_price))
    price = Field(input_processor=Compose(TakeFirst(), get_price), output_processor=TakeFirst())
    size = Field(output_processor=TakeFirst())


class SkuItem(scrapy.Item):
    def __setitem__(self, key, value):
        print key
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(SkuItem, self).__setitem__(key, value)
