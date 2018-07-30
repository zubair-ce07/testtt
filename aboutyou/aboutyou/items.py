import scrapy


class AboutyouItem(scrapy.Item):
    gender = scrapy.Field()
    category = scrapy.Field()
    # Product Item
    product_url = scrapy.Field()            # str: URL of the currency product
    store_keeping_unit = scrapy.Field()     # str: unique ID that might be used in database of the website
    title = scrapy.Field()                  # str: Title of the product
    brand = scrapy.Field()                  # str: Brand of the product (site name if brand not given explicitly)
    description = scrapy.Field()            # list: List of strings in normalized form
    locale = scrapy.Field()                 # str: language and country e.g; en_GB, en_US, en_PK
    currency = scrapy.Field()               # str: currency code of the selected locale. e.g; USD, PKR etc.
    variations = scrapy.Field()             # dict: { <slugified_color_name>: <List of Variation Items> ... }
