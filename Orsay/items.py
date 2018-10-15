from scrapy import Field, Item


class OrsayItem(Item):
    """Item class which contains all the required
    fields which has to be crawled from the website
    """
    _id = Field()    # Defined id for checking repetition
    brand = Field()
    care = Field()
    category = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
