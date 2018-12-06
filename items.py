import scrapy

class DocketSpiderItem(scrapy.Item):
    
    docket_id = scrapy.Field()
    filer = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
