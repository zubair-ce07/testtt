# -*- coding: utf-8 -*-
"""
Items for using in the HMScrapper
"""
from scrapy import Item, Field


class HmScrapperItem(Item):
    """
    Item object to scrape by HMSpider
    """
    name = Field()
    price = Field()
    concept = Field()
    discount = Field()
    care_info = Field()
    item_code = Field()
    old_price = Field()
    color_skus = Field()
    description = Field()
    composition = Field()
