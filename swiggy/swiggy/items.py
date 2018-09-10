# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class ProductItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    restaurant = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    category_description = scrapy.Field()
    subcategory_description = scrapy.Field()
    special_category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()
    veg = scrapy.Field()
    price = scrapy.Field()
    discounted_price = scrapy.Field()
    store_id = scrapy.Field()
    pincode = scrapy.Field()
    locality = scrapy.Field()
    city = scrapy.Field()
    sku = scrapy.Field()
    thumbnail = scrapy.Field()
    date_of_crawl = scrapy.Field()
    promotion = scrapy.Field()
    offer = scrapy.Field()
    average_rating = scrapy.Field()
    num_of_ratings = scrapy.Field()
    min_order = scrapy.Field()


class BannerItem(scrapy.Item):
    pincode = scrapy.Field()
    url = scrapy.Field()
    city = scrapy.Field()
    crawl_time = scrapy.Field()
    rank = scrapy.Field()
    thumbnail = scrapy.Field()
    redirect_url = scrapy.Field()
    restaurant_field = scrapy.Field()


def clean(self, values):
    return [value.strip() for value in values]


class MenuItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    title_in = clean


class BannerItemLoader(ItemLoader):
    default_item_class = BannerItem
    default_output_processor = TakeFirst()

