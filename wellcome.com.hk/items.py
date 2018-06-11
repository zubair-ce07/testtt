import scrapy
import re

from scrapy.loader.processors import TakeFirst, Join, MapCompose, Compose, Identity
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class HonestbeeItem(scrapy.Item):
    url = scrapy.Field()
    code = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_price = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    availability = scrapy.Field()
    packaging = scrapy.Field()
    image_urls = scrapy.Field()
    reviews_count = scrapy.Field()
    reviews_score = scrapy.Field()
    barcode = scrapy.Field()
    store_name = scrapy.Field()
    website_name = scrapy.Field()
    product_type = scrapy.Field()
    price_per_unit = scrapy.Field()


def _clean_in(loader, values):
    return [x.strip() if isinstance(values, str) else x for x in values if x]


class HonestbeeItemLoader(ItemLoader):
    default_item_class = HonestbeeItem
    default_input_processor = _clean_in
    default_output_processor = TakeFirst()
    description_out = Join(', ')
    previous_price_out = Join(', ')
    categories_out = Join(' | ')
    image_urls_out = Join(' | ')
