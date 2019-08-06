import re
import json
from datetime import datetime

from scrapy.spiders import Spider

from lanebryant.items import LaneBryantItem


class LaneBryantParser(Spider):
    name = "lanebryant_parser"

    currency = "CA"
    retailer = "lanebryant-ca"
    lang = "en"
    market = "CA"

    gender = "Women"

    def parse(self, response):
        garment = LaneBryantItem()
        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = self.get_image_urls(response)
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.lang
        garment["currency"] = self.currency
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.gender
        garment["price"] = self.get_product_price(response)
        garment["skus"] = self.get_product_skus(response)

        yield garment

    def clean(self, text):
        regex = r"\r\n|\r|\n|\\|\\'|\.|\$"
        return re.sub(regex, "", text)

    def raw_product(self, response):
        css = "script:contains('@context')::text"
        return json.loads(self.clean(response.css(css).get())[:-2])

    def raw_sku(self, response):
        css = "#pdpInitialData::text"
        return json.loads(response.css(css).get())["pdpDetail"]["product"][0]

    def get_product_name(self, response):
        return response.css(".mar-product-title::text").get().strip()

    def get_product_description(self, response):
        return [self.raw_product(response)["description"]]

    def get_retailer_sku(self, response):
        return self.raw_product(response)["sku"]

    def get_product_price(self, response):
        return self.clean(self.raw_product(response)["offers"]["price"])

    def get_product_care(self, response):
        css = ".mar-product-additional-info #tab1 li:not(:first-child)::text"
        return [care.strip() for care in response.css(css).getall()]

    def get_product_brand(self, response):
        return self.raw_product(response)["brand"]

    def get_product_category(self, response):
        css = "script:contains('window.lanebryantDLLite')"
        category = response.css(css).re_first('pageName": "(.+?)"')
        return category.replace(" ", "").split(":")

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_previous_price(self, parsed_json):
        return self.clean(parsed_json['list_price']) \
            if parsed_json['list_price'] != parsed_json["sale_price"] else None

    def get_image_urls(self, response):
        images = []
        raw_sku = self.raw_sku(response)["all_available_colors"][0]["values"]

        base_images = [images["sku_image"].replace("//", "", 2)
                       for images in raw_sku]

        for image in base_images:
            images += [
                image,
                image + '_Back',
                image + '_alt1'
            ]

        return images

    def get_product_pricing(self, parsed_json):
        previous_price = self.get_previous_price(parsed_json)
        pricing = {
            "price": self.clean(parsed_json["sale_price"]),
            "currency": self.currency
        }
        if previous_price:
            pricing['previous_price'] = previous_price

        return pricing

    def get_product_color_sizes(self, response):
        color_size = {}
        raw_sku = self.raw_sku(response)

        color_size.update({colors["id"]: colors["name"]
                          for colors in raw_sku["all_available_colors"][0]["values"]})
        color_size.update({sizes["id"]: sizes["value"]
                          for sizes in raw_sku["all_available_sizes"][0]["values"]})
        return color_size

    def get_product_skus(self, response):
        skus = {}
        parsed_json = self.raw_sku(response)

        common_sku = self.get_product_pricing(parsed_json["skus"][0]["prices"])
        color_sizes = self.get_product_color_sizes(response)

        for item in parsed_json["skus"]:
            sku = common_sku.copy()

            sku["color"] = color_sizes[item['color']]
            sku["size"] = color_sizes[item['size']] if color_sizes[item['size']] else item['size']

            if not parsed_json["isSellable"]:
                sku["out_of_stock"] = True

            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
