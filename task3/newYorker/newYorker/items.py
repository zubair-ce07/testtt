import scrapy


class NewyorkerItem(scrapy.Item):
    id = scrapy.Field()
    country = scrapy.Field()
    maintenance_group = scrapy.Field()
    web_category_id = scrapy.Field()
    web_category = scrapy.Field()
    brand = scrapy.Field()
    sales_unit = scrapy.Field()
    customer_group = scrapy.Field()
    variants = scrapy.Field()
