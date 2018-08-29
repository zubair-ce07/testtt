from scrapy.item import Item, Field


class ProductItem(Item):
    referrer_url = Field()
    brand = Field()
    product_name = Field()
    care = Field()
    url = Field()
    category = Field()
    currency = Field()
    description = Field()
    image_urls = Field()
    retailer_sku = Field()
    color_id = Field()
    color_name = Field()
    skus = Field()


class SizeItem(Item):
    size_identifier = Field()
    size_name = Field()
    stock = Field()
    full_price = Field()
    sale_price = Field()

