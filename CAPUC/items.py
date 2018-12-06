# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    assignees=scrapy.Field()
    description=scrapy.Field()
    crawled_at=scrapy.Field()
    end_time=scrapy.Field()
    filed_on=scrapy.Field()
    filings=scrapy.Field()
    industries=scrapy.Field()
    job_id=scrapy.Field()
    major_parties=scrapy.Field()
    modified=scrapy.Field()
    proceeding_type=scrapy.Field()
    request_fingerprint=scrapy.Field()
    run_id=scrapy.Field()
    slug=scrapy.Field()
    source_assignees=scrapy.Field()
    source_major_parties=scrapy.Field()
    source_title=scrapy.Field()
    source_url=scrapy.Field()
    spider_name=scrapy.Field()
    start_time=scrapy.Field()
    state=scrapy.Field()
    state_id=scrapy.Field()
    status=scrapy.Field()
    synch=scrapy.Field()
    title=scrapy.Field()
    uploaded=scrapy.Field()
    states=scrapy.Field()
    meta=scrapy.Field()
    pass
