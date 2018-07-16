import json

import scrapy
from scrapy.loader.processors import MapCompose


def create_sku_jsonobject_from_jsonstring(sku_jsonstring):
    sku_jsonobject = json.loads(sku_jsonstring)
    filtered_sku_jsonobject = {
        "colour": sku_jsonobject.get("option0", 'None'),
        "price": sku_jsonobject.get("price_number", 'None'),
        "Currency": "Brazilian real",
        "size": sku_jsonobject.get("option1", 'None'),
        "previous_price": sku_jsonobject.get("compare_at_price_short", 'None'),
        "sku_id": sku_jsonobject.get("sku", 'None')
        }

    return filtered_sku_jsonobject


def get_gender_from_url(url):
    if 'Unisex' in url:
        return 'Unisex'

    if 'masculino' in url:
        return 'boy'

    return 'girl'


def get_category_from_name(product_name):
    if product_name:
        return product_name.split(" ")[0]


def convert_price_to_cents(product_price):
    if product_price:
        return float(product_price[2:].replace(',', '')) * 100


def decode_non_ascii(des):
    if des:
        return unicodedata.normalize("NFKD", des)


class ProductItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(decode_non_ascii))
    brand = scrapy.Field()
    description = scrapy.Field(input_processor=MapCompose(decode_non_ascii))
    category = scrapy.Field(input_processor=MapCompose(get_category_from_name))
    price = scrapy.Field(input_processor=MapCompose(convert_price_to_cents))
    url = scrapy.Field()
    gender = scrapy.Field(input_processor=MapCompose(get_gender_from_url))
    skus = scrapy.Field(input_processor=MapCompose(create_sku_jsonobject_from_jsonstring),
                        output_processor=lambda x: x)
    image_urls = scrapy.Field(output_processor=lambda x: x)
