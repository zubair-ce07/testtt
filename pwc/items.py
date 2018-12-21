# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    categories=scrapy.Field()
    company=scrapy.Field()
    crawled_at=scrapy.Field()
    description=scrapy.Field()
    external_id=scrapy.Field()
    job_date=scrapy.Field()
    job_types=scrapy.Field()
    location=scrapy.Field()
    logo_urls=scrapy.Field()
    provider=scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
