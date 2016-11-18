import json
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from runners_point.items import RunnersPointItem


class RunnersPointSpider(CrawlSpider):
    name = "runnerspoint"
    allowed_domains = ["runnerspoint.de"]
    start_urls = [
        "https://www.runnerspoint.de/de/p/adidas-originals-tubular-nova-primeknit-herren-sneakers-40701?v=55802406"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=["#nav", ".pagination"])),
        Rule(LinkExtractor(restrict_css=".product-image"), callback="parse_item")
    )

    def parse(self, response):
        raw_data = response.xpath("//script[contains(., 'doRelay42AddProducts')]").re_first("\((\[.*\])\)")
        runners_point_data = json.loads(raw_data.replace("\'", '"'))

        item = RunnersPointItem()

        item["url"] = response.url
        item["spider_name"] = "runnerspoint-de-crawl"
        item["retailer"] = "runnerspoint-de"
        item["brand"] = runners_point_data[0]["brand"]
        item["market"] = "DE"
        item["lang"] = "de"
        item["currency"] = "EUR"
        item["category"] = runners_point_data[0]["category"].split("/")
        item["name"] = runners_point_data[0]["name"]
        item["description"] = response.css(
            ".fl-product-details--description--column p:nth-child(2)::text").extract_first()
        item["gender"] = runners_point_data[0]["gender"]
        item["price"] = runners_point_data[0]["price"]
        item["skus"] = {}
        item["image_urls"] = self.get_images_urls(response)

        variants = self.get_variants(runners_point_data)

        return self.fetch_ajax_data(variants, item)

    def get_images_urls(self, response):
        all_srcs = []

        srcs = response.css(".fl-picture source::attr(srcset)").extract()

        for src in srcs:
            if "//" in src:
                all_srcs.append(src)

        return all_srcs

    @staticmethod
    def get_variants(runners_point_data):
        variants = []
        for variant in runners_point_data:
            variants.append(variant["variant"])

        return variants

    def fetch_ajax_data(self, variants, item):
        if variants:
            variant = variants.pop()
            variant_id = variant.split("_")[1]
            return scrapy.Request(
                "https://www.runnerspoint.de/INTERSHOP/web/WFS/Runnerspoint-Runnerspoint_DE-Site/de_DE/-/EUR/ViewProduct-ProductVariationSelect?BaseSKU=" + variant_id + "&InventoryServerity=ProductDetail&ajax=1&page=1"
                , callback=self.parse_ajax, meta={"variants": variants, "item": item})
        return item

    def parse_ajax(self, response):
        data = json.loads(response.text)
        selector = scrapy.Selector(text=data["content"], type="html")
        sizes = selector.css(".fl-product-size span::text").extract()

        item = response.meta["item"]
        variants = response.meta["variants"]

        item["skus"].update(self.get_skus(variants, item, sizes))

        return self.fetch_ajax_data(variants, item)

    @staticmethod
    def get_skus(variants, item, sizes):
        skus = {}

        for size in sizes:
            for variant in variants:
                color = variant.split("_")[0]
                skus[color + "_" + size] = {
                    "currency": "EUR",
                    "price": item["price"],
                    "size": size,
                    "color": color
                }

        return skus
