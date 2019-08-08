import scrapy


class JobItem(scrapy.Item):
    crawl_id = scrapy.Field()
    crawled_at = scrapy.Field()
    title = scrapy.Field()
    job_nature = scrapy.Field()
    attribute = scrapy.Field()
    job_count = scrapy.Field()
