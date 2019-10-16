from scrapy import Item, Field


class SixthstreetItem(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()  
    description = Field() 
    care = Field()
    skus = Field()
    image_urls = Field()
