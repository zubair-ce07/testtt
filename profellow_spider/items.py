import scrapy


class Fellowship(scrapy.Item):
    crawled_at = scrapy.Field()
    deadline = scrapy.Field()
    description = scrapy.Field()
    disciplines = scrapy.Field()
    experience = scrapy.Field()
    external_id = scrapy.Field()
    fellowship_organization = scrapy.Field()
    fellowship_url = scrapy.Field()
    keywords = scrapy.Field()
    location = scrapy.Field()
    provider = scrapy.Field()
    site_record_url = scrapy.Field()
    title = scrapy.Field()
