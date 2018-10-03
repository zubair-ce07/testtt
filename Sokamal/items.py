"""Script for Item Loading for Sokamal's products"""
import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def filter_image_urls(value):
    """Filters image_urls received as string"""
    img_urls = []
    if value and len(value) > 1:
        img_url = json.loads(value)
        for url in img_url.values():
            img_urls.append("https://fishry-image.azureedge.net/product/" + url['Image'])
    return img_urls


def filter_category(value):
    """Filters category received as string"""
    categories = []
    if value:
        category = json.loads(value)
        for category in category.values():
            categories.append(category['name'])
    return categories


def filter_url(value):
    """Filters url received as string"""
    return "https://sokamal.com/product/" + value


def filter_skus(value):
    """Filters sku received as string"""
    skus = {}
    if value:
        sku_data = json.loads(value)
        for sku in sku_data:
            inventory_quantity = sku['inventoryQuantity']
            barcode = sku['barcode']
            price = sku['price']
            size, color = filter_color_size(sku)
            skus[barcode] = {
                "color": color,
                "size": size,
                "price": price,
                "currency": "Rs",
                "inventory_quantity": inventory_quantity
            }
    return skus


def filter_color_size(value):
    """Filters color_size received as list"""
    size_color = value['name']
    color = "generic"
    if len(size_color) > 1:
        color = size_color.pop()
        size = size_color.pop()
        return size, color
    return size_color[0], color


class SokamalItem(scrapy.Item):
    """SoKamal Item Class"""
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    retailer_sku = scrapy.Field()
    care = scrapy.Field()
    category = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    barcode = scrapy.Field()


class SokamalLoader(ItemLoader):
    """SoKamal ItemLoader Class"""
    default_output_processor = TakeFirst()
    default_item_class = SokamalItem
    description_in = MapCompose(remove_tags)
    image_urls_in = MapCompose(filter_image_urls)
    category_in = MapCompose(filter_category)
    url_in = MapCompose(filter_url)
    skus_in = MapCompose(filter_skus)
