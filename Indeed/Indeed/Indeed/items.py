# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    crawl_id = scrapy.Field()
    crawl_time = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    attribute = scrapy.Field()
    job_count = scrapy.Field()
