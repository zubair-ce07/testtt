import json
import re
import urllib.parse
from datetime import datetime

from w3lib.url import add_or_replace_parameter

from childrensplace.items import ChildrensPlaceItem
from scrapy import Request
from scrapy.spiders import CrawlSpider


class Mixin():
    name = "childrensplace"
    allowed_domains = ['childrensplace.com', "search.unbxd.io"]
    start_urls = ['http://www.childrensplace.com/us/home/']
    retailer = "childrensplace-us"
    market = "US"
    category_req = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/category?"
    variant_req = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/search?"


class ChildrensPlaceParser(Mixin):
    name = Mixin.name + "-parser"

    def parse_product(self, response):
        details = json.loads(response.body)["response"]["products"]
        product_details = {
            "uuid": self.product_id(details),
            "retailer_sku": self.retailer_sku(details),
            "name": self.product_name(details),
            "description": self.product_description(details),
            "crawl_id": f"childrensplace-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj",
            "market": self.market,
            "retailer": self.retailer,
            "retailer_sku": self.retailer_sku(details),
            "categories": self.product_categories(details),
            "gender": self.get_gender(details),
            "spider_name": self.name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "crawl_start_time": datetime.now().isoformat(),
            "url": self.product_url(details, response)
        }
        item = ChildrensPlaceItem(product_details)
        return self.parse_colors(details, item)

    def skus(self, product):
        skus = []
        for variant in product["variants"]:
            sku = self.pricing_details(variant)
            sku["color"] = variant["auxdescription"]
            sku["size"] = variant["v_tcpsize"]
            sku["sku_id"] = f"{variant['auxdescription']}_{variant['v_tcpsize']}"
            skus.append(sku)
        return skus

    def parse_colors(self, details, item):
        item["skus"] = []
        item["image_urls"] = []
        for product in details:
            item["skus"] = item["skus"] + self.skus(product)
            item["image_urls"].append(self.image_urls(product))
        yield item

    def product_name(self, details):
        return details[0]["product_name"]

    def product_price(self, details):
        return details[0]["min_offer_price"]

    def pricing_details(self, details):
        return {
            "price": int(float(details["v_offerprice"])) * 100,
            "previous_price": int(float(details["v_listprice"])) * 100,
            "currency": details["v_currency"]}

    def retailer_sku(self, details):
        return details[0]["style_partno"]

    def product_id(self, details):
        return details[0]["uniqueId"]

    def product_url(self, details, response):
        return f"http://www.childrensplace.com/us/p/{details[0]['seo_token']}"

    def product_description(self, details):
        return [details[0]["product_short_description"]]

    def product_categories(self, details):
        return details[0]["categoryPath2"]

    def get_gender(self, details):
        return details[0]["gender"]

    def image_urls(self, details):
        return details["imageUrl"][0]


class ChildrensPlaceCrawler(CrawlSpider, Mixin):
    name = Mixin.name + "-crawler"
    parser = ChildrensPlaceParser()

    def parse(self, response):
        main_data = self.get_home_page_data(response)
        naviagtion_details = main_data["globalComponents"]["header"][
            "navigationTree"]
        category_map = self.category_map(naviagtion_details)

        for cat_id, sub_categories in category_map.items():
            for sub_category in sub_categories:
                for sub_id, url in sub_category.items():
                    yield Request(
                        url=response.urljoin(url), callback=self.parse_listing,
                        meta={"category": cat_id, "sub_category": sub_id})

    def get_home_page_data(self, response):
        site_data = re.findall(
            "window.__PRELOADED_STATE__ = (.+?);\n", response.body.decode(
                "utf-8"))[0]
        return json.loads(site_data)

    def category_map(self, naviagtion_details):
        category_map = {}
        for detail in naviagtion_details:
            category_map[detail["categoryId"]] = [
                {sub["categoryId"]: sub["url"]} for sub in detail["menuItems"][0]]
        return category_map

    def parse_listing(self, response):
        meta = response.meta
        parameters = {
            "start": 0, "rows": 100, "pagetype": "boolean",
            "p-id": f'categoryPathId:"{meta["category"]}>{meta["sub_category"]}"'}
        request_url = f"{self.category_req}{urllib.parse.urlencode(parameters)}"

        yield Request(url=request_url, callback=self.parse_details, meta={"page": 0})

    def parse_details(self, response):
        parameters = {"variants": True, "variants.count": 100, "pagetype": "boolean"}
        details = json.loads(response.body)["response"]

        for product in details["products"]:
            parameters["q"] = product["style_partno"]
            request_url = f"{self.variant_req}{urllib.parse.urlencode(parameters)}"
            yield Request(url=request_url, callback=self.parser.parse_product)

        page = response.meta["page"]
        if (page + 100) < int(details["numberOfProducts"]):
            url = add_or_replace_parameter(response.url, "start", page + 100)
            yield Request(url=url, callback=self.parse_details, meta={"page": page + 100})
