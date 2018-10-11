import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class IsetanItem(scrapy.Item):
    _id = scrapy.Field()    # Defined id for checking repetition
    image_urls = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    categories = scrapy.Field()
    product_type = scrapy.Field()
    currency = scrapy.Field()
    pass


def clean_text(self, info):
    values = [re.sub('\s+', ' ', text).strip() for text in info if text]
    return [text for text in values if text]


class IsetanItemLoader(ItemLoader):
    default_item_class = IsetanItem
    default_input_processor = clean_text
    description_out = TakeFirst()
    quantity_out = TakeFirst()