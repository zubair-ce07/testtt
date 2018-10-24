import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from shopjusticebot.items import ShopjusticeProduct


class ShopjusticeSpider(CrawlSpider):
    name = "shopjustice"
    allowed_domains = ["shopjustice.com"]
    start_urls = ["http://www.shopjustice.com"]

    listings_css = [".mar-nav a", ".nextPage"]
    products_css = ".mar-prd-item-image-container"

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_product")
    )

    def parse_product(self, response):
        product = ShopjusticeProduct()
        product["product_id"] = self.product_id(response)
        product["gender"] = "women"
        product["brand"] = "Shopjustice"
        product["name"] = self.product_name(response)
        product["url"] = response.url
        product["care"] = self.product_care(response)
        product["description"] = self.product_description(response)
        raw_product = self.raw_product(response)
        product["image_urls"] = self.image_urls(response)
        product["category"] = self.product_category(raw_product)

        if self.is_out_of_stock(raw_product):
            product["out_of_stock"] = True

        product["skus"] = self.skus(raw_product)
        yield product

    def product_id(self, response):
        return response.css("#pdpProductID::attr(value)").extract_first()

    def product_name(self, response):
        return response.css(".jst-product-title::text").extract_first()

    def product_description(self, response):
        description = response.css("#tab1")

        if description:
            return description[0].css("li::text").extract()

    def product_care(self, response):
        return response.css("#tab2 li::text").extract()

    def image_urls(self, response):
        raw_image_urls = self.raw_product(response)
        return [raw_image["sku_image"] for raw_image in
                raw_image_urls["all_available_colors"][0]["values"]]

    def product_category(self, raw_category):
        return raw_category["ensightenData"][0]["categoryPath"].split(":")

    def colours(self, raw_colour, key):
        available_colour = raw_colour["all_available_colors"][0]["values"]
        return [colour["name"] for colour in available_colour] if key == "name" \
            else [colour["id"] for colour in available_colour]

    def sizes(self, raw_sizes):
        available_sizes = raw_sizes["all_available_sizes"][0]["values"]
        return [size["value"] for size in available_sizes]

    def raw_product(self, response):
        raw_product = response.css("#pdpInitialData::text").extract_first()
        return json.loads(raw_product)["pdpDetail"]["product"][0]

    def skus(self, raw_skus):
        colours = self.colours(raw_skus, "name")
        sizes = self.sizes(raw_skus)
        common_sku = self.product_pricing(raw_skus)
        skus = {}
        for colour in colours:
            for size in sizes:
                sku = common_sku.copy()
                sku["size"] = size
                sku["colour"] = colour
                skus[f"{sku['colour']}_{sku['size']}"] = sku
        return skus

    def product_pricing(self, raw_prices):
        prices = {}
        values = raw_prices["all_available_colors"][0]["values"][0]["prices"]
        prices["currency"] = re.findall(r"([^0-9.])", values["sale_price"])[0]
        prices["price"] = float(values["sale_price"][1:])

        if float(values["list_price"][1:]) != prices["price"]:
            prices["previous_price"] = float(values["list_price"][1:])

        return prices

    def is_out_of_stock(self, raw_product):
        return not raw_product["ensightenData"][0]["productAvailable"] == 'true'
