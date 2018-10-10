import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class LululemonItem(scrapy.Item):
    _id = scrapy.Field()    # Defined id for checking repetition
    brand = scrapy.Field()
    care = scrapy.Field()
    fabric = scrapy.Field()
    features = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    is_new = scrapy.Field()
    is_sold_out = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    default_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    pass


def clean_text(self, info):
    values = [re.sub('\s+', ' ', text).strip() for text in info if text]
    return [text for text in values if text]


class LululemonItemLoader(ItemLoader):
    default_item_class = LululemonItem
    description_in = clean_text
    fabric_in = clean_text
    features_in = clean_text
    care_in = clean_text
