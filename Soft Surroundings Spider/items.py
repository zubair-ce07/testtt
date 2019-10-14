from scrapy import Item, Field


class SoftsurroundingsItem(Item):
    retailer_sku = Field()
    gender = Field()
    category = Field()
    brand = Field()
    url = Field()
    name = Field()  
    description = Field() 
    care = Field()
    skus = Field()
    requests = Field()
    image_urls = Field()
