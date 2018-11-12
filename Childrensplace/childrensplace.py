import json
import re
from datetime import datetime
from urllib.parse import urlencode

from w3lib.url import add_or_replace_parameter

from childrensplace.items import ChildrensPlaceItem
from scrapy import Request
from scrapy.spiders import CrawlSpider


class Mixin:
    allowed_domains = ["childrensplace.com", "search.unbxd.io"]
    start_urls = ["http://www.childrensplace.com/us/home/"]

    retailer = "childrensplace-us"
    market = "US"

    category_req_url_t = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/category?{0}"
    variant_req_url_t = "https://search.unbxd.io/8870d5f30d9bebafac29a18cd12b801d"\
        "/childrensplace-com702771523455856/search?{0}"
    product_url_t = "http://www.childrensplace.com/us/p/{0}"
    image_url_t = "https://www.childrensplace.com/wcsstore/GlobalSAS/images/tcp/"\
        "products/500/{0}"


class ChildrensPlaceParser(Mixin):
    name = Mixin.retailer + "-parser"

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
        item["gender"] = self.product_gender(product_details)
        item["spider_name"] = Mixin.retailer
        item["date"] = datetime.now().strftime("%Y-%m-%d")
        item["crawl_start_time"] = datetime.now().isoformat()
        item["url"] = self.product_url(product_details)

        return self.color_variants(product_details, item)

    def skus(self, color_variant):
        skus = []

        for size_variant in color_variant["variants"]:
            sku = self.product_pricing(size_variant)
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
            item["image_urls"] += self.image_urls(color_variant)

        yield item

    def product_name(self, product_details):
        return product_details[0]["product_name"]

    def product_price(self, product_details):
        return product_details[0]["min_offer_price"]

    def product_pricing(self, product_details):
        return {
            "price": int(float(product_details["v_offerprice"]) * 100),
            "previous_price": int(float(product_details["v_listprice"]) * 100),
            "currency": product_details["v_currency"]}

    def retailer_sku(self, product_details):
        return product_details[0]["style_partno"]

    def product_id(self, product_details):
        return product_details[0]["uniqueId"]

    def product_url(self, product_details):
        return self.product_url_t.format(product_details[0]['seo_token'])

    def product_description(self, product_details):
        return [product_details[0]["product_short_description"]]

    def product_categories(self, product_details):
        return product_details[0]["categoryPath2"]

    def product_gender(self, product_details):
        return product_details[0]["gender"]

    def get_crawl_id(self):
        return f"childrensplace-us-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj"

    def image_urls(self, product_details):
        return product_details["imageUrl"] + [self.image_url_t.format(
            img) for img in json.loads(product_details["alt_img"]).values()]


class ChildrensPlaceCrawler(CrawlSpider, Mixin):
    name = Mixin.retailer + "-crawler"
    parser = ChildrensPlaceParser()
    PAGE_SIZE = 100

    def parse(self, response):
        main_data = self.raw_listings(response)
        naviagtion_details = main_data["globalComponents"]["header"][
            "navigationTree"]
        category_map = self.map_category(naviagtion_details)

        for cat_id, sub_categories in category_map.items():
            yield self.category_requests(cat_id, sub_categories, response)

    def category_requests(self, cat_id, sub_categories, response):
        for sub_category in sub_categories:
            return response.follow(
                sub_category[0], callback=self.parse_listing,
                meta={"category": cat_id, "sub_category": sub_category[1]})

    def raw_listings(self, response):
        script = "window.__PRELOADED_STATE__ = (.+?);\n"
        site_data = re.findall(script, response.body.decode("utf-8"))[0]
        return json.loads(site_data)

    def map_category(self, naviagtion_details):
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
        request_url = self.category_req_url_t.format(urlencode(parameters))

        yield Request(request_url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        parameters = {"variants": True, "variants.count": self.PAGE_SIZE, "pagetype": "boolean"}
        product_list = json.loads(response.body)["response"]
        product_requests = self.parse_products(parameters, product_list)

        for page in range(0, product_list["numberOfProducts"], self.PAGE_SIZE):
            url = add_or_replace_parameter(response.url, "start", page)
            product_requests.append(Request(url, callback=self.parse_pagination))

        return product_requests

    def parse_products(self, parameters, product_list):
        product_requests = []

        for product_details in product_list["products"]:
            parameters["q"] = product_details["style_partno"]
            request_url = self.variant_req_url_t.format(urlencode(parameters))
            product_requests.append(Request(request_url, callback=self.parser.parse_product))

        return product_requests
