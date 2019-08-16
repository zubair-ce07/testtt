import copy
import json
import re
from urllib.parse import urljoin
from urllib.parse import urlsplit
from w3lib.url import add_or_replace_parameter

import scrapy
from scrapy.spiders import Spider

from ScrapySawitfirst.items import Item


class SawItFirstParser(Spider):
    name = "sawitfirstitemparser"
    color_request_url = "https://4uiusmis27.execute-api.eu-central-1.amazonaws.com/isaw/get-colours"
    product_request_url = "https://www.isawitfirst.com/products/"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://www.isawitfirst.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
                       (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.99"
    }
    care_raw = ["%", "machine", "wash", "wipe", "clean", "hand"]
    category_hitsperpage = 60
    prodpage_bottom_hitsperpage = 15
    uid = "ATT_1564987309510_06771628066488389"
    sid = "db4jx5c7ut"
    fields_category = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"
    fields_prodpage_bottom = "id, handle, image, title, tags, FSM_compare_at_price, FSM_price, FSM_OnSale"

    def parse_item(self, response):
        product = Item()
        product['retailer_sku'] = self.retailer_sku(response)
        product['gender'] = self.gender()
        product['category'] = self.category(response)
        product['brand'] = self.brand(response)
        product['url'] = self.url(response)
        product['name'] = self.product_name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        product['price'] = self.price(response)
        product['previous_prices'] = self.previous_prices(response)
        product['currency'] = self.currency(response)
        product['skus'] = {}
        form_data = {"jl_numbers": re.findall(r"-(jl\d+-?\d*)$", response.url), "site": "isawitfirst.com"}
        self.headers["Referer"] = response.url
        request = scrapy.http.JSONRequest(self.color_request_url,
                                          callback=self.parse_sku_requests,
                                          data=form_data, headers=self.headers
                                          )
        request.meta["product"] = product
        yield request

    def parse_next_page(self, response):
        page_data = json.loads(response.text)
        page_data = page_data["zones"][0]["data"]["metadata"]
        url = response.meta["url"]
        hits = int(page_data["hits"])
        hitsperpage = int(page_data["hitsperpage"])
        first = int(page_data["first"])
        if (first + hitsperpage) < hits:
            url = urlsplit(url).geturl()
            if first == 0:
                next_page = 1
            else:
                next_page = (first / hitsperpage) + 1
            url = add_or_replace_parameter(url, 'page', f"{next_page}")
            yield scrapy.Request(url, callback=self.parse)

    def prepare_params(self, response):
        category_re = r'data-attraqt-category="(\w+[-?\w*]*)"'
        params = {
            "siteid": response.css(".page-collection::attr(data-attraqt-site-id)").extract_first(),
            "pageurl": response.url,
            "zone0": re.findall(r'data-attraqt-page-type="(\w+)"', response.text)[0],
            "sid": self.sid,
            "uid": self.uid,
            "config_category": re.findall(category_re, response.text)[0],
            "config_categorytree": re.findall(category_re, response.text)[0]
        }
        if params["zone0"] == "category":
            params["fields_category"] = self.fields_category
            params["category_hitsperpage"] = self.category_hitsperpage
            params["category_page"] = int(re.findall(r"page=(\d+)$", response.url)[0]) + 1
        else:
            params["fields_prodpage_bottom"] = self.fields_prodpage_bottom
            params["prodpage_bottom_hitsperpage"] = self.prodpage_bottom_hitsperpage
            params["sku"] = re.findall(r'"resourceId":(\d+)}', response.text)[0]
        return params

    def retailer_sku(self, response):
        return response.css(".product-sku > *::text").extract_first()

    def category(self, response):
        categories_str = re.findall("Categories: (.+),", response.text)[0]
        return re.findall(r'"\s*([^"]*?)\s*"', categories_str)

    def brand(self, response):
        return re.findall(r'Brand: "(.+)",', response.text)[0]

    def url(self, response):
        return response.url

    def product_name(self, response):
        return re.findall(r'Name: "(.+)",', response.text)[0]

    def description(self, response):
        return response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()

    def care(self, response):
        description = response.xpath('//*[*[@class="product-description-title"]]/p/text()').extract()
        return [d for d in description if any(cr in d.lower() for cr in self.care_raw)]

    def image_urls(self, response):
        return response.css(".slide-item img::attr(src)").getall()

    def price(self, response):
        price_text = response.css("[data-handle=sale-price]::text").extract_first()
        return self.format_price(price_text)

    def previous_prices(self, response):
        prices = response.css(".old-price::text").extract()
        prices = set([self.format_price(p) for p in prices])
        return list(prices)

    def format_price(self, price):
        return int(price.replace(u'\u00A3', '').replace(".", ''))

    def currency(self, response):
        return response.css('[property=og\:price\:currency]::attr(content)').extract_first()

    def gender(self):
        return "women"

    def color(self, response, variants):
        for product in variants["products"]:
            if product['handle'] in response.url:
                return product["colour_name"]

    def stock(self, response):
        quantities = [int(q) for q in response.css(".product-size option::attr(data-quantity)").extract()]
        sizes = [s.strip() for s in response.css(".size-list .value::text").extract() if s.strip()]
        stock = []
        for size, quantity in zip(sizes, quantities):
            stock.append((size, quantity))
        return stock

    def parse_sku_requests(self, response):
        product = response.meta["product"]
        colours = json.loads(response.text)
        for colour in colours["products"]:
            request = scrapy.Request(urljoin(self.product_request_url, colour['handle']), callback=self.parse_skus)
            request.meta["product"] = product
            request.meta["variants_info"] = colours
            yield request

    def parse_skus(self, response):
        product = response.meta["product"]
        variants = response.meta["variants_info"]
        color = self.color(response, variants)
        price = self.price(response)
        previous_prices = self.previous_prices(response)
        currency = self.currency(response)
        stock = self.stock(response)
        sku = {"colour": color, "price": price, 'previous_prices': previous_prices, "currency": currency}
        for size, quantity in stock:

            sku["size"] = size
            if quantity == 0:
                sku["out_of_stock"] = True
            else:
                sku["out_of_stock"] = False
            product["skus"][f"{color}_{size}"] = copy.deepcopy(sku)
        if len(product["skus"]) == len(variants["products"]) * len(stock):
            yield product

