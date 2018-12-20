import re

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class GreatfoodhallItem(Item):
    """Item class which contains all the required
    fields which has to be crawled from the website
    """
    _id = Field()    # Defined id for checking repetition
    image_url = Field()
    flag_image = Field()
    name = Field()
    website = Field()
    url = Field()
    price = Field()
    nutrition_info_values = Field()
    nutrition_info_fields = Field()
    quantity = Field()
    categories = Field()
    product_type = Field()
    currency = Field()
    availability = Field()


def clean_name(text):
    return text.strip()


def clean_price(text):
    return "".join(re.findall(r"([^\d.])", text))


def check_availablility(self, text):
    if text:
        return "Out of stock"
    else:
        return "Available"


def clean_image_url(self, value, loader_context):
    return [loader_context['response'].urljoin(url) for url in value]


def clean_info(self, info):
    values = [re.sub('\s+', ' ', text).strip() for text in info if text]
    return [text for text in values if text]


def clean_category_text(self, category):
    category = "".join(category).strip()
    category = category.split(">")
    return [cat.strip() for cat in category]


class GreatfoodhallLoader(ItemLoader):
    default_item_class = GreatfoodhallItem
    name_in = MapCompose(clean_name)
    currency_in = MapCompose(clean_price)
    nutrition_info_values_in = clean_info
    nutrition_info_fields_in = clean_info
    quantity_out = TakeFirst()
    categories_in = clean_category_text
    product_type = TakeFirst()
    image_url_in = clean_image_url
    flag_image_in = clean_image_url
    availability_in = check_availablility
