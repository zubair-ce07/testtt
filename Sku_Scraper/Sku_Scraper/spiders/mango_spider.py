import json
import re

import scrapy
from scrapy.loader import ItemLoader
from w3lib.url import urljoin, add_or_replace_parameter

from ..items import Product


class MangoParseSpider(scrapy.Spider):
    name = "mango_parse_spider"
    seen_ids = set()
    gender_map = {
            "m": "women",
            "h": "men",
            "a": "girls",
            "e" : "girls",
            "o" : "boys",
            "d" : "boys",
            "v" : "unisex-adults"
        }

    def parse(self, response):
        raw_product = self.extract_raw_product(response)
        product_id = self.extract_pid(raw_product)

        if self.is_seen_item(product_id):
            return

        product_loader = ItemLoader(item=Product(), response=response)
        product_loader.add_value("pid", product_id)

        gender = self.detect_gender(raw_product)
        product_loader.add_value("gender", gender)

        url = self.extract_url(response)
        product_loader.add_value("url", url)

        name = self.extract_name(response)
        product_loader.add_value("name", name)

        description = self.extract_description(raw_product)
        product_loader.add_value("description", description)

        requests = self.extract_colour_requests(response) \
                 + self.extract_category_requests(response)

        product_loader.add_value("meta", {"requests" : requests})
        return self.get_request_or_item(product_loader)

    def parse_colour(self, response):
        product_loader = response.meta["item_loader"]
        raw_colour = json.loads(response.text)

        image_urls = self.extract_image_urls(raw_colour)
        product_loader.add_value('image_urls', image_urls)

        skus = self.extract_skus(raw_colour)
        product_loader.add_value('skus', skus)

        return self.get_request_or_item(product_loader)

    def parse_category(self, response):
        product_loader = response.meta["item_loader"]

        category = self.extract_category(response)
        product_loader.add_value('category', category)
        
        return self.get_request_or_item(product_loader)

    def extract_raw_product(self, response):
        script_x = '//script[contains(., "var dataLayerV2Json")]/text()'
        raw_product_s = response.xpath(script_x).re_first(r'{.*}')
        raw_product = json.loads(raw_product_s)
        return raw_product["ecommerce"]["detail"]["products"]

    def extract_colour_requests(self, response):
        stock_id = self.extract_stock_id(response)

        raw_product = self.extract_raw_product(response)
        session_id = self.extract_pid(raw_product)

        colour_url = response.urljoin(f"/services/garments/{session_id}")
        request = scrapy.Request(colour_url, callback=self.parse_colour)
        request.headers["stock-id"] = stock_id

        return [request]

    def extract_category_requests(self, response):
        stock_id = self.extract_stock_id(response)

        raw_product = self.extract_raw_product(response)
        session_id = self.extract_pid(raw_product)

        category_url = response.urljoin(f"/services/garments/{session_id}/breadcrumb")
        request = scrapy.Request(category_url, callback=self.parse_category)
        request.headers["stock-id"] = stock_id

        return [request]

    def get_request_or_item(self, product_loader):
        item = product_loader.load_item()
        requests_queue = product_loader.item["meta"]["requests"]

        if requests_queue:
            request = requests_queue.pop()
            request.meta["item_loader"] = product_loader
            return request

        del item["meta"]
        return item     

    def extract_stock_id(self, response):
        script_x = "//script[contains(., 'viewObjectsJson')]/text()"
        raw_session = json.loads(response.xpath(script_x).re(r'{.*}')[2])
        raw_stock_id = raw_session["headerMenusParams"]["optionalParams"]["cacheId"]
        return ".".join(raw_stock_id.split(".")[2:8])
    
    def extract_pid(self, raw_product):
        return raw_product["id"]

    def is_seen_item(self, product_id):
        if product_id in self.seen_ids:
            return True

        self.seen_ids.add(product_id)

    def detect_gender(self, raw_product):
        gender = raw_product["gender"]

        for key, value in self.gender_map.items():
            if key == gender.lower():
                return value

        return "unisex-adults"

    def extract_url(self, response):
        css = '[property="og:url"]::attr(content)'
        return response.css(css).extract_first()

    def extract_name(self, response):
        css = '[property="og:title"]::attr(content)'
        return response.css(css).extract_first()

    def extract_category(self, response):
        raw_category = json.loads(response.text)
        return [(rc["text"]) for rc in raw_category["breadcrumb"]]   

    def extract_description(self, raw_product):
        return raw_product["description"].split(",") 

    def extract_image_urls(self, raw_colour):
        colours = raw_colour["colors"]["colors"]
        return [url for colour in colours for url in colour["images"]]

    def extract_skus(self, raw_colour):
        skus = []
        price = raw_colour["price"]["price"]
        currency = raw_colour["price"]["currency"]

        common_skus = {
            "currency" :currency,
            "price" : price
        }

        raw_skus = raw_colour["colors"]["colors"]
        for raw_sku in raw_skus:
            colour = raw_sku["label"]
            common_skus["color"] = colour

            for raw_size in raw_sku["sizes"]:

                if raw_size["id"] == "-1":
                    continue

                sku = common_skus.copy()

                size = raw_size["value"]
                sku["size"] = size

                if not raw_size.get("available"):
                    sku["out_of_stock"] = True

                sku["sku_id"] = f"{colour}_{size}" if colour else size
                skus.append(sku)

        return skus

    
class MangoCrawlSpider(scrapy.Spider):
    name = "mango_crawl_spider"
    start_urls = ["https://shop.mango.com/services/menus/header/GB",
                  "https://www.mangooutlet.com/services/menus/header/GB"] 

    allowed_domains = ["mangooutlet.com", "mango.com"]
    parse_spider = MangoParseSpider()

    def parse(self, response):
        raw_menu = json.loads(response.text)
        yield from self.make_category_requests(raw_menu)
                
    def parse_categories(self, response):
        raw_category = self.extract_raw_listings(response)

        shop_id = raw_category["idShop"]
        section_id = raw_category["idSection"]

        url = response.urljoin(f"services/productlist/products/GB/{shop_id}/{section_id}")

        if "idSubSection" in raw_category["optionalParams"]:
            sub_section_id = raw_category["optionalParams"]["idSubSection"]
            url = add_or_replace_parameter(url, "idSubSection", sub_section_id) 

        yield scrapy.Request(url, callback=self.parse_listings)

    def parse_listings(self, response):
        raw_listings = json.loads(response.text)
        raw_listings = raw_listings["groups"][0]["garments"]

        for raw_listing in raw_listings.values():
            listing = raw_listing["colors"][0]["linkAnchor"]
            yield scrapy.Request(listing, callback=self.parse_item)

    def parse_item(self, response):
        return self.parse_spider.parse(response)

    def make_category_requests(self, raw_menu):
        for menu_text, sub_menu in raw_menu.items():

            if menu_text == "link" and "retroId" in raw_menu:
                yield scrapy.Request(sub_menu, callback=self.parse_categories)

            if isinstance(sub_menu, (dict, list)):
                sub_menu = sub_menu if isinstance(sub_menu, list) else [sub_menu]    

                for s_menu in sub_menu:  
                    if not isinstance(s_menu, dict):
                        continue

                    yield from self.make_category_requests(s_menu)

    def extract_raw_listings(self, response):
        script_x = "//script[contains(., 'viewObjectsJson')]/text()"
        raw_category = response.xpath(script_x).re(r'{.*}')[2]
        return json.loads(raw_category)["catalogParameters"]
