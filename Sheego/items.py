import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class SheegoItem(Item):

    _id = Field()    # Defined id for checking repetition
    brand = Field()
    care = Field()
    categories = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()


def clean_text(self, description):
    values = [re.sub('\s+', ' ', text).strip() for text in description if text]
    return [text for text in values if text]


class SheegoItemLoader(ItemLoader):
    default_item_class = SheegoItem
    description_in = clean_text
    care_in = clean_text
    categories_in = clean_text
