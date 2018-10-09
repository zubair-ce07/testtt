import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class SheegoItem(scrapy.Item):

    _id = scrapy.Field()    # Defined id for checking repetition
    brand = scrapy.Field()
    care = scrapy.Field()
    categories = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    pass


def clean_text(self, description):
    values = [re.sub('\s+', ' ', text).strip() for text in description if text]
    return [text for text in values if text]


class SheegoItemLoader(ItemLoader):
    default_item_class = SheegoItem
    description_in = clean_text
    care_in = clean_text
    categories_in = clean_text
