import scrapy


class JobItem(scrapy.Item):
    crawl_id = scrapy.Field()
    crawl_time = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    attribute = scrapy.Field()
    job_count = scrapy.Field()
