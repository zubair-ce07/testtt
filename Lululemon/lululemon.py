import json

import w3lib.url

import scrapy
from lululemon.items import LululemonItem, LululemonItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LululemonSpider(CrawlSpider):
    name = 'lululemon'
    allowed_domains = ['shop.lululemon.com']
    start_urls = ['http://shop.lululemon.com/']

    rules = (Rule(LinkExtractor(
            allow=('view-all')),
            callback='parse_product_list'),
    )

    def parse_product_list(self, response):
        yield scrapy.Request(
            url="https://shop.lululemon.com/api/c/men/_/N-7tu",     # Men
            callback=self.extract_product_urls,
        )
        yield scrapy.Request(
            url="https://shop.lululemon.com/api/c/women/_/N-7vf",   # Women
            callback=self.extract_product_urls,
        )
        yield scrapy.Request(
            url="https://shop.lululemon.com/api/c/girls/_/N-8gr",   # Girls
            callback=self.extract_product_urls,
        )

    def extract_product_urls(self, response):
        json_data = json.loads(response.body)
        records = json_data[
            "data"]["attributes"]["main-content"][0]["records"]

        for record in records:
            yield scrapy.Request(
                url=response.urljoin(f"/api{record['pdp-url']}"),
                callback=self.parse_product,
            )
        if response.url is not response.urljoin(json_data["links"]["last"]):
            yield scrapy.Request(
                url=response.urljoin(f"/api{json_data['links']['next']}"),
                callback=self.extract_product_urls
            )

    def is_available(self, sku, attr):
        color_driver = attr["purchase-attributes"]["color-driver"]
        for color in color_driver:
            if color["color"] == sku["color-code"] and sku["size"] in color["sizes"]:
                return True
        return False

    def develop_skus(self, response, json_data):
        attr = json_data["data"]["attributes"]
        all_colors = attr["purchase-attributes"]["all-color"]
        child_skus = attr["child-skus"]
        skus = {}

        for sku in child_skus:
            skus[f"{sku['color-code']}_{sku['size']}"] = {
                "color_id": sku['color-code'],
                "color_name": [
                    color["display-name"] for color in
                    all_colors if color["color-code"] == sku['color-code']],
                "size": sku['size'],
                "currency": "USD ($)",
                "price": sku["price-details"]["list-price"],
                "on sale": sku["price-details"]["on-sale"],
                "style_id": sku["style-id"],
                "is_available": self.is_available(sku, attr)
            }
        return skus

    def parse_product(self, response):
        json_data = json.loads(response.body)
        product_summary = json_data[
            "data"]["attributes"]["product-summary"]
        product_attr = json_data[
            "data"]["attributes"]["product-attributes"]

        loader = LululemonItemLoader(item=LululemonItem(), response=response)
        loader.add_value("_id", product_summary["product-id"])
        loader.add_value("name", product_summary["display-name"])
        loader.add_value("title", product_summary["title"])
        loader.add_value("brand", "lululemon")
        loader.add_value("default_sku", product_summary["default-sku"])
        loader.add_value("is_new", product_summary["is-new"])
        loader.add_value("is_sold_out", product_summary["is-sold-out"])
        loader.add_value("category", product_summary["product-category"])
        loader.add_value("description", product_summary["why-we-made-this"])
        loader.add_value("image_urls", product_summary["sku-sku-images"])
        loader.add_value(
            "fabric",
            product_attr["product-content-fabric"][0]["fabricDescription"])
        loader.add_value(
            "care",
            [c["careDescription"] for c in
                product_attr["product-content-care"][0]["care"] if c])
        loader.add_value(
            "features",
            [f["featureDescription"] for f in
                product_attr["product-content-feature"][0]["f5Features"] if f])
        loader.add_value("website", self.start_urls)
        loader.add_value("skus", self.develop_skus(response, json_data))
        yield loader.load_item()
