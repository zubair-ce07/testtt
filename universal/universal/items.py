# -*- coding: utf-8 -*-
import scrapy


def clean_categories(categories):
    return list(
        filter(
            lambda x: '...' not in x,
            categories
        )
    )


class UniversalItem(scrapy.Item):
    url = scrapy.Field()
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    image_urls = scrapy.Field()
    product_sku = scrapy.Field()
    care = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()
    category = scrapy.Field(serializer=clean_categories)
