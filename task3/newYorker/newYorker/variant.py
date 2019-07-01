import scrapy


class NewyorkerItemsVariant(scrapy.Item):
    id = scrapy.Field()
    product_id = scrapy.Field()
    publish_date = scrapy.Field()
    new_in = scrapy.Field()
    coming_soon = scrapy.Field()
    sale = scrapy.Field()
    color_name = scrapy.Field()
    pantone_color = scrapy.Field()
    pantone_color_name = scrapy.Field()
    red = scrapy.Field()
    green = scrapy.Field()
    blue = scrapy.Field()
    color_group = scrapy.Field()
    basic_color = scrapy.Field()
    currency = scrapy.Field()
    original_price = scrapy.Field()
    current_price = scrapy.Field()
    red_price_change = scrapy.Field()
    sizes = scrapy.Field()
    images = scrapy.Field()
