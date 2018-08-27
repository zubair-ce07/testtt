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
    skus = Field()


class SizeItem(Item):
    size_id = Field()
    size_name = Field()
    color = Field()
    stock = Field()
    full_price = Field()
    sale_price = Field()

