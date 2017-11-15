# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapytaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HypedcItem(scrapy.Item):

    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    product_code = scrapy.Field()
    price_final = scrapy.Field()
    desc = scrapy.Field()
    color = scrapy.Field()
    currency = scrapy.Field()
    image_urls = scrapy.Field()
    sizes_info = scrapy.Field()

class SkechersItem(scrapy.Item):

    Style_Name = scrapy.Field()
    Style_Brand = scrapy.Field()
    Style_Category = scrapy.Field()
    Style_URL = scrapy.Field()
    Style_Product_Code = scrapy.Field()
    Style_Price_Final = scrapy.Field()
    Style_Desc = scrapy.Field()
    Style_Color = scrapy.Field()
    Style_Currency = scrapy.Field()
    Style_Image_Urls = scrapy.Field()
    Style_Sizes_Info = scrapy.Field()
    Style_More_Details = scrapy.Field()
