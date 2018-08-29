from scrapy import Item, Field


class HugobossScraperItem(Item):
    retailer_sku = Field()
    name = Field()
    image_urls = Field()
    lang = Field()
    gender = Field()
    category = Field()
    industry = Field()
    brand = Field()
    url = Field()
    market = Field()
    trail = Field()
    retailer = Field()
    url_original = Field()
    description = Field()
    care = Field()
    skus = Field()
