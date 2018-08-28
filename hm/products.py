from scrapy import Item
from scrapy import Field


class Product(Item):
    brand = Field()
    category = Field()
    description = Field()
    image_urls = Field()
    name = Field()
    skus = Field()
    url = Field()
    color_name = Field()
    base_sku =Field()



class Size_Item(Item):
    size_name = Field()
    full_price = Field()
    sale_price = Field()
    in_stock = Field()
