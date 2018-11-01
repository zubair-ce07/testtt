import json
import re
import urllib.parse
from datetime import datetime

from w3lib.url import add_or_replace_parameter

from childrensplace.items import ChildrensPlaceItem
from scrapy import Request
from scrapy.spiders import CrawlSpider


class Mixin:
    name = "childrensplace"
    allowed_domains = ['childrensplace.com', "search.unbxd.io"]
    start_urls = ['http://www.childrensplace.com/us/home/']
    retailer = "childrensplace-us"
    market = "US"

    category_req_url = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/category?"
    variant_req_url = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/search?"


class ChildrensPlaceParser(Mixin):
    name = Mixin.name + "-parser"

    def parse_product(self, response):
        product_details = json.loads(response.body)["response"]["products"]
        item = ChildrensPlaceItem()
        item["uuid"] = self.product_id(product_details)
        item["retailer_sku"] = self.retailer_sku(product_details)
        item["name"] = self.product_name(product_details)
        item["description"] = self.product_description(product_details)
        item["crawl_id"] = self.get_crawl_id()
        item["market"] = self.market
        item["retailer"] = self.retailer
        item["retailer_sku"] = self.retailer_sku(product_details)
        item["categories"] = self.product_categories(product_details)
        item["gender"] = self.get_gender(product_details)
        item["spider_name"] = self.name
        item["date"] = datetime.now().strftime("%Y-%m-%d")
        item["crawl_start_time"] = datetime.now().isoformat()
        item["url"] = self.product_url(product_details)

        return self.color_variants(product_details, item)

    def skus(self, color_variant):
        skus = []
        for size_variant in color_variant["variants"]:
            sku = self.pricing_details(size_variant)
            sku["color"] = size_variant["auxdescription"]
            sku["size"] = size_variant["v_tcpsize"]
            sku["sku_id"] = f"{size_variant['auxdescription']}_{size_variant['v_tcpsize']}"
            skus.append(sku)
        return skus

    def color_variants(self, product_details, item):
        item["skus"] = []
        item["image_urls"] = []
        for color_variant in product_details:
            item["skus"] += self.skus(color_variant)
            item["image_urls"].append(self.image_urls(color_variant))
        yield item

    def product_name(self, product_details):
        return product_details[0]["product_name"]

    def product_price(self, product_details):
        return product_details[0]["min_offer_price"]

    def pricing_details(self, product_details):
        return {
            "price": int(float(product_details["v_offerprice"])) * 100,
            "previous_price": int(float(product_details["v_listprice"])) * 100,
            "currency": product_details["v_currency"]}

    def retailer_sku(self, product_details):
        return product_details[0]["style_partno"]

    def product_id(self, product_details):
        return product_details[0]["uniqueId"]

    def product_url(self, product_details):
        return f"http://www.childrensplace.com/us/p/{product_details[0]['seo_token']}"

    def product_description(self, product_details):
        return [product_details[0]["product_short_description"]]

    def product_categories(self, product_details):
        return product_details[0]["categoryPath2"]

    def get_gender(self, product_details):
        return product_details[0]["gender"]

    def get_crawl_id(self):
        return f"childrensplace-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"

    def image_urls(self, product_details):
        return product_details["imageUrl"][0]


class ChildrensPlaceCrawler(CrawlSpider, Mixin):
    name = Mixin.name + "-crawler"
    parser = ChildrensPlaceParser()
    PAGE_SIZE = 100

    def parse(self, response):
        main_data = self.get_home_page_data(response)
        naviagtion_details = main_data["globalComponents"]["header"][
            "navigationTree"]
        category_map = self.category_map(naviagtion_details)

        for cat_id, sub_categories in category_map.items():
            for sub_category in sub_categories:
                    yield response.follow(
                        sub_category[0], callback=self.parse_listing,
                        meta={"category": cat_id, "sub_category": sub_category[1]})

    def get_home_page_data(self, response):
        script = "window.__PRELOADED_STATE__ = (.+?);\n"
        site_data = re.findall(script, response.body.decode("utf-8"))[0]
        return json.loads(site_data)

    def category_map(self, naviagtion_details):
        category_map = {}
        for menu in naviagtion_details:
            category_map[menu["categoryId"]] = [
                [sub["url"], sub["categoryId"]] for sub in menu["menuItems"][0]]
        return category_map

    def parse_listing(self, response):
        meta = response.meta
        parameters = {
            "start": 0, "rows": self.PAGE_SIZE, "pagetype": "boolean",
            "p-id": f'categoryPathId:"{meta["category"]}>{meta["sub_category"]}"'}
        request_url = f"{self.category_req_url}{urllib.parse.urlencode(parameters)}"

        yield Request(request_url, callback=self.parse_details, meta={"page": 0})

    def parse_details(self, response):
        parameters = {"variants": True, "variants.count": self.PAGE_SIZE, "pagetype": "boolean"}
        json_response = json.loads(response.body)["response"]

        for product_details in json_response["products"]:
            parameters["q"] = product_details["style_partno"]
            request_url = f"{self.variant_req_url}{urllib.parse.urlencode(parameters)}"
            yield Request(request_url, callback=self.parser.parse_product)

        page = response.meta["page"]
        start = page + self.PAGE_SIZE
        if start < int(json_response["numberOfProducts"]):
            url = add_or_replace_parameter(response.url, "start", start)
            yield Request(url, callback=self.parse_details, meta={"page": start})
