import scrapy


class DocketItem(scrapy.Item):
    docket_id = scrapy.Field()
    description = scrapy.Field()
    filer = scrapy.Field()
    file_url = scrapy.Field()
    date_filed = scrapy.Field()
