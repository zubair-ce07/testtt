import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class IsetanItem(Item):
    image_urls = Field()
    name = Field()
    brand = Field()
    website = Field()
    description = Field()
    url = Field()
    price = Field()
    quantity = Field()
    categories = Field()
    product_type = Field()
    currency = Field()


def clean_text(self, info):
    values = [re.sub('\s+', ' ', text).strip() for text in info if text]
    return [text for text in values if text]


def find_currency(self, text):
    return re.findall(r"[^\d.]", text[0])


class IsetanItemLoader(ItemLoader):
    default_item_class = IsetanItem
    default_input_processor = clean_text
    quantity_out = TakeFirst()
    currency_in = find_currency
