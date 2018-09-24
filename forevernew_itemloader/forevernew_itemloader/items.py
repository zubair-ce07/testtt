from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Compose


def skus_process(raw_skus):
    price_css = ".regular-price .price:not([id])::text, .special-price .price:not([id])::text"
    prev_price_css = ".old-price .price:not([id])::text"
    skus = {}
    common_sku = {"currency": "USD"}

    for sku_id, raw_sku in raw_skus.items():
        sku = common_sku.copy()
        sku["price"] = float(raw_sku['price'].css(price_css).extract_first().strip("$ \n"))
        sku["colour"] = raw_sku["colour"]
        prev_price = raw_sku["price"].css(prev_price_css).extract()

        if prev_price:
            sku["previous_prices"] = [float(price.strip("$ \n")) for price in prev_price]

        if not raw_sku["sizes"]:
            sku["size"] = "One Size"
            skus[sku_id] = sku

        for size_s in raw_sku["sizes"]:
            size_sku = sku.copy()
            size_sku["size"] = size_s.css("::text").extract_first().split(": ")[1].strip().split(" (")[0]

            if size_s.css(".out-of-stock"):
                size_sku["out-of-stock"] = True

            skus[f"{sku_id}_{size_sku['size']}"] = size_sku

    return skus


class ProductItem(Item):
    retailer_sku = Field(output_processor=TakeFirst(), input_processor=MapCompose(lambda sku: sku.split("#")[1]))
    lang = Field(output_processor=TakeFirst())
    trail = Field()
    gender = Field(output_processor=TakeFirst())
    category = Field()
    brand = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    date = Field()
    market = Field(output_processor=TakeFirst())
    url_original = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    description = Field()
    care = Field(input_processor=Compose(lambda care_input: [care for care in care_input if care.strip()]))
    image_urls = Field()
    skus = Field(output_processor=TakeFirst(), input_processor=MapCompose(lambda raw_sku: skus_process(raw_sku)))
    out_of_stock = Field(output_processor=TakeFirst())
    price = Field(output_processor=TakeFirst(), input_processor=MapCompose(lambda price: float(price.strip("$ \n"))))
    currency = Field(output_processor=TakeFirst())
