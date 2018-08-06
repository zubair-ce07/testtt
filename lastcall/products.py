from scrapy import Item
from scrapy import Field


class ProductItem(Item):
    brand = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    name = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
    color = Field()


class SizeItem(Item):
    size_name = Field()
    full_price = Field()
    sale_price = Field()
    in_stock = Field()
