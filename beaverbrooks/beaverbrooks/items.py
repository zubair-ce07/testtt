import scrapy


class BeaverbrooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Product(scrapy.Item):
    """
    Product represents a blueprint for every product available
    on the site
    """

    product_image = scrapy.Field()
    product_title = scrapy.Field()
    product_offer_price = scrapy.Field()
    product_offer_per_month = scrapy.Field()
    product_specification = scrapy.Field()
    product_code = scrapy.Field()
