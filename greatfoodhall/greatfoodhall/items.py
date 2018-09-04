from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Compose


class GreatfoodhallItem(Item):
    url = Field()
    brand = Field()
    name = Field()
    price = Field()
    currency = Field()
    previous_price = Field()
    categories = Field()
    packaging = Field()
    image_urls = Field()
    website_name = Field()
    availability = Field()


def clean_categories(self, categories):
    categories_soup = "".join(categories)
    categories = categories_soup.strip()
    return categories.split(">")


class GreatfoodhallItemLoader(ItemLoader):
    default_item_class = GreatfoodhallItem
    default_output_processor = TakeFirst()

    price_in = MapCompose(lambda price: price.split("$")[1])
    previous_price_in = MapCompose(lambda price: price.split("$")[1])
    image_urls_out = Identity()
    categories_out = Identity()
    categories_in = clean_categories
    availability_in = Compose(lambda stock_out: True if stock_out else False)
