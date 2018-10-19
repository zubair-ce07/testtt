import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request

from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = "eloquii"
    allowed_domains = ["www.eloquii.com"]
    start_urls = ["https://www.eloquii.com"]

    merch_map = [
        ("limited edition", "Limited Edition"),
        ("special edition", "Special Edition")
    ]
    skus_req_url_t = "https://www.eloquii.com/on/demandware.store/Sites-eloquii-Site/" \
                    "default/Product-GetVariants?pid={}&format=json"

    listings_css = ["#nav_menu", ".row.justify-content-center.mt-5"]
    products_css = ".product-images"

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_product")
    )

    def parse_product(self, response):
        if not self.is_available(response):
            return

        product = EloquiiProduct()
        product["product_id"] = self.product_id(response)
        product["brand"] = "Eloquii"
        product["name"] = self.product_name(response)
        product["category"] = self.product_category(response)
        product["description"] = self.product_description(response)
        product["url"] = response.url
        product["image_urls"] = self.image_urls(response)
        product["skus"] = {}
        product["merch_info"] = self.merch_info(product)

        if self.is_out_of_stock(response):
            product["out_of_stock"] = True

        yield Request(url=self.skus_req_url_t.format(product["product_id"]),
                      callback=self.parse_skus, meta={"product": product})

    def product_id(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-product-id)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-name)"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = ".breadcrumb span[itemprop=title]::text"
        return response.css(css).extract()[1:]

    def product_description(self, response):
        css = "[name=description]::attr(content)"
        return response.css(css).extract_first().split(",")

    def image_urls(self, response):
        css = "#bt_pdp_main > script::text"
        raw_images = response.css(css).re(r"\"large\" :(\[[\s\w\D]*?\])")
        return [url["url"] for raw_url in raw_images for url in json.loads(raw_url)]

    def merch_info(self, product):
        soup = " ".join(product["name"] + "".join(product["description"])).lower()
        return [merch for merch_str, merch in self.merch_map if merch_str in soup]

    def is_available(self, response):
        return not bool(re.search(r"\'COMINGSOON\': (true)", response.text))

    def is_out_of_stock(self, response):
        css = "[property='og:availability']::attr(content)"
        return not "IN_STOCK" in response.css(css).extract()

    def parse_skus(self, response):
        product = response.meta["product"]
        raw_prodcut = json.loads(response.text)
        raw_skus = raw_prodcut["variations"]["variants"]
        product["skus"] = self.skus(raw_skus)
        yield product

    def skus(self, raw_skus):
        skus = {}
        for data in raw_skus:
            sku = self.product_pricing(data)
            sku["color"] = data["attributes"]["colorCode"]
            sku["size"] = data["attributes"]["size"]

            if not data["inStock"]:
                sku["out_of_stock"] = not data["inStock"]

            skus["_".join(data["attributes"].values())] = sku
        return skus

    def product_pricing(self, json_data):
        prices = {}
        previous_price = json_data["pricing"]["standard"]
        prices["price"] = json_data["pricing"]["sale"]
        prices["currency"] = "$"

        if previous_price != prices["price"]:
            prices["previous_price"] = previous_price

        return prices
