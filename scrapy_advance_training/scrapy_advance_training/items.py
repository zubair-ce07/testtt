# -*- coding = Field()utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Field, Item


class ProductItem(Item):
    new_price_text = Field()
    category_names = Field()
    currency = Field()
    referer_url = Field()
    size_infos = Field()
    country_code = Field()
    language_code = Field()
    sku = Field()
    full_price_text = Field()
    title = Field()
    base_sku = Field()
    old_price_text = Field()
    available = Field()
    old_identifier = Field()
    color_code = Field()
    brand = Field()
    image_urls = Field()
    description_text = Field()
    url = Field()
    color_name = Field()
    identifier = Field()


class SizeInfosItem(Item):
    size_name = Field()
    size_identifier = Field()
    stock = Field()
