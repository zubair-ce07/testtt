import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst


class GreatfoodhallItem(scrapy.Item):
    """Item class which contains all the required
    fields which has to be crawled from the website
    """

    _id = scrapy.Field()    # Defined id for checking repetition
    image_url = scrapy.Field()
    flag_image = scrapy.Field()
    name = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    nutrition_info_values = scrapy.Field()
    nutrition_info_fields = scrapy.Field()
    quantity = scrapy.Field()
    categories = scrapy.Field()
    product_type = scrapy.Field()
    currency = scrapy.Field()
    availability = scrapy.Field()
    pass


def clean_name(text):
    return text.strip()


def clean_price(text):
    return text.replace("HK$", "")


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
    price_in = MapCompose(clean_price)
    nutrition_info_values_in = clean_info
    nutrition_info_fields_in = clean_info
    quantity_out = TakeFirst()
    categories_in = clean_category_text
    product_type = TakeFirst()
    image_url_in = clean_image_url
    flag_image_in = clean_image_url
    availability_in = check_availablility
