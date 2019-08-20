import re
import json
from datetime import datetime

from scrapy.spiders import Spider

from lanebryant.items import LaneBryantItem


class LaneBryantParser(Spider):
    name = "lanebryant_parser"

    currency = "CAD"
    retailer = "lanebryant-ca"
    lang = "en"
    market = "CA"

    gender = "Women"

    def parse(self, response):
        garment = LaneBryantItem()
        raw_sku = self.raw_sku(response)
        raw_product = self.raw_product(response)

        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(raw_product)
        garment["retailer_sku"] = self.get_retailer_sku(raw_product)
        garment["image_urls"] = self.get_image_urls(raw_sku)
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.lang
        garment["currency"] = self.currency
        garment["brand"] = self.get_product_brand(raw_product)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.gender
        garment["price"] = self.get_product_price(raw_product)
        garment["skus"] = self.get_product_skus(raw_sku)

        yield garment

    def clean(self, text):
        regex = r"\r\n|\r|\n|\\|\\'|\.|\$|\  +"
        return re.sub(regex, "", text)

    def raw_product(self, response):
        css = "script:contains('@context')::text"
        return json.loads(self.clean(response.css(css).get())[:-2])

    def raw_sku(self, response):
        css = "#pdpInitialData::text"
        return json.loads(response.css(css).get())["pdpDetail"]["product"][0]

    def get_product_name(self, response):
        return response.css(".mar-product-title::text").get().strip()

    def get_product_description(self, raw_product):
        return [self.clean(raw_product["description"])]

    def get_retailer_sku(self, raw_product):
        return raw_product["sku"]

    def get_product_price(self, raw_product):
        return self.clean(raw_product["offers"]["price"])

    def get_product_care(self, response):
        css = ".mar-product-additional-info #tab1 li:not(:first-child)::text"
        return [care.strip() for care in response.css(css).getall()]

    def get_product_brand(self, raw_product):
        return raw_product["brand"]

    def get_product_category(self, response):
        css = "script:contains('window.lanebryantDLLite')"
        category = response.css(css).re_first('pageName": "(.+?)"')
        return category.replace(" ", "").split(":")

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_previous_price(self, parsed_json):
        return self.clean(parsed_json['list_price']) \
            if parsed_json['list_price'] != parsed_json["sale_price"] else None

    def get_image_urls(self, raw_sku):
        images = []
        raw_images = raw_sku["all_available_colors"][0]["values"]

        base_images = [images["sku_image"].replace("//", "", 2)
                       for images in raw_images]

        for image in base_images:
            images += [image, f"{image}_Back", f"{image}_alt1"]
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

    def variant_map(self, raw_sku, sku_id, sku_list):
        return {variant["id"]: variant[sku_id]
                for variant in raw_sku[sku_list][0]["values"]}

    def get_product_skus(self, raw_sku):
        skus = {}

        common_sku = self.get_product_pricing(raw_sku["skus"][0]["prices"])
        colour_map = self.variant_map(raw_sku, "name", "all_available_colors")
        size_map = self.variant_map(raw_sku, "value", "all_available_sizes")

        for item in raw_sku["skus"]:
            sku = common_sku.copy()

            sku["color"] = colour_map[item['color']]
            sku["size"] = size_map[item['size']] if size_map[item['size']] else item['size']

            if not raw_sku["isSellable"]:
                sku["out_of_stock"] = True

            skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
