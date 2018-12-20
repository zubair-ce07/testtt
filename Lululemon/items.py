import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class LululemonItem(Item):
    _id = Field()    # Defined id for checking repetition
    brand = Field()
    care = Field()
    fabric = Field()
    features = Field()
    category = Field()
    description = Field()
    is_new = Field()
    is_sold_out = Field()
    image_urls = Field()
    name = Field()
    title = Field()
    default_sku = Field()
    skus = Field()
    url = Field()
    website = Field()


def clean_text(self, info):
    values = [re.sub('\s+', ' ', text).strip() for text in info if text]
    return [text for text in values if text]


class LululemonItemLoader(ItemLoader):
    default_item_class = LululemonItem
    description_in = clean_text
    fabric_in = clean_text
    features_in = clean_text
    care_in = clean_text
