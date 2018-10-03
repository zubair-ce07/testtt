# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity


class BaseItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    size = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    image_urls = scrapy.Field()
    meta_data = scrapy.Field()
    gallery = scrapy.Field()
    medium = scrapy.Field()
    framing = scrapy.Field()
    authenticity = scrapy.Field()
    website_name = scrapy.Field()
    images = scrapy.Field()
    current_bid_price = scrapy.Field()
    auction_name = scrapy.Field()
    biography = scrapy.Field()
    artist_image = scrapy.Field()


def _clean_in(loader, values):
    values = [re.sub('\s+', ' ', x).strip() for x in values if x]
    return [x for x in values if x]


class BaseItemLoader(ItemLoader):
    default_item_class = BaseItem
    default_input_processor = _clean_in
    default_output_processor = Join(' ')
    title_out = TakeFirst()
    size_out = TakeFirst()
    price_out = TakeFirst()
    type_out = TakeFirst()
    image_urls_out = Identity()
    images_out = Identity()
    artist_image_out = TakeFirst()
