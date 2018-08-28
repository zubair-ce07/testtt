from json import loads
import time

from scrapy import Spider, FormRequest
from w3lib.url import urljoin

from ..items import ProductItem


class WoolrichProductParserSpider(Spider):
    name = "woolrich-product-parser"
    sku_base_url = "https://www.woolrich.com/remote/v1/product-attributes/"
    currency = "USD"
    seen_skus = set()
    gender_map = {
        " men ": "men",
        " women ": "women",
        "default": "unisex"
    }

    def parse(self, response):
        product = ProductItem()
        product_id = self.product_id(response)

        if product_id in self.seen_skus:
            return None

        self.seen_skus.add(product_id)
        product["retailer_sku"] = product_id
        product["lang"] = "en"
        product["trail"] = response.meta.get("trail", [])
        product["gender"] = self.gender(response)
        product["category"] = self.category(response)
        product["brand"] = "Woolrich"
        product["url"] = response.url
        product["date"] = int(time.time())
        product["market"] = "US"
        product["url_original"] = response.url
        product["name"] = self.product_name(response)
        product["description"] = self.description(response)
        product["care"] = self.care(response)
        product["image_urls"] = self.images(response)
        product["skus"] = {}
        sku_requests = self.sku_requests(response)

        if sku_requests:
            product["price"] = self.price(response)
            product["currency"] = self.currency
        else:
            product["out_of_stock"] = True

        return self.prepare_request(sku_requests, product)

    def parse_sku(self, response):
        product = response.meta["product"]
        product["skus"].update(self.sku(response))
        product["image_urls"].append(self.sku_image(response))
        return self.prepare_request(response.meta["requests"], product)

    def sku(self, response):
        raw_sku = loads(response.text)["data"]
        sku_price = raw_sku["price"]
        sku_id = raw_sku["sku"]
        sku = {
            "colour": response.meta["colour"],
            "size": response.meta['size'],
            "price": int(sku_price["without_tax"]["value"] * 100),
            "currency": self.currency
        }

        if sku_price.get("rrp_without_tax"):
            sku["previous_prices"] = [int(sku_price["rrp_without_tax"]["value"] * 100)]

        if not raw_sku["instock"]:
            sku["out_of_stock"] = True

        return {sku_id: sku}

    @staticmethod
    def sku_image(response):
        image = loads(response.text)["data"].get("image")

        if image:
            return image["data"].replace("{:size}", "1200x1318")
        return None

    def sku_requests(self, response):
        raw_skus = self.raw_skus(response)
        product_id = response.css("[name='product_id']::attr('value')").extract_first()
        sku_url = urljoin(self.sku_base_url, product_id)
        requests = []

        for raw_sku in raw_skus:
            request = FormRequest(url=sku_url, formdata=raw_sku["form-data"],
                                  callback=self.parse_sku)
            request.meta["colour"] = raw_sku["colour"]
            request.meta["size"] = raw_sku.get("size", "One size")
            requests.append(request)

        return requests

    @staticmethod
    def prepare_request(requests, product):
        if requests:
            request = requests.pop()
            request.meta["product"] = product
            request.meta["requests"] = requests
            yield request
        else:
            yield product

    @staticmethod
    def images(response):
        return response.css(".zoom ::attr(src)").extract()

    @staticmethod
    def price(response):
        return int(float(response.css("[itemprop='price']::attr(content)").extract_first()) * 100)

    @staticmethod
    def care(response):
        return response.css("#features-content >::text").extract()

    @staticmethod
    def description(response):
        return response.css("#details-content::text").extract_first()

    @staticmethod
    def product_name(response):
        return response.css(".productView-title::text").extract_first()

    def gender(self, response):
        gender_soup = " ".join(self.category(response)).lower()

        for gender in self.gender_map:
            if gender in gender_soup:
                return self.gender_map[gender]

        return self.gender_map["default"]

    @staticmethod
    def category(response):
        return response.css(".breadcrumb-label::text").extract()

    @staticmethod
    def product_id(response):
        return response.css("strong:contains(Style)::text").extract_first().split("#: ")[1]

    @staticmethod
    def raw_skus(response):
        skus_colour_s = response.css("[data-cart-item-add] [data-product-attribute='swatch']")
        skus_size_s = response.css("[data-cart-item-add] [data-product-attribute='set-rectangle']")
        raw_skus = []

        for colour_s in skus_colour_s.css("input[name]"):
            value = colour_s.css("::attr(value)").extract_first()
            raw_skus.append({
                "form-data": {colour_s.css("::attr(name)").extract_first(): value},
                "colour": skus_colour_s.css(f"[for*='{value}'] ::attr(title)").extract_first()
            })

        for size_op_s in skus_size_s:
            skus = raw_skus.copy()
            raw_skus = []

            for raw_sku in skus:
                for size_s in size_op_s.css("input[name]"):
                    sku = raw_sku.copy()
                    form_data = sku["form-data"].copy()
                    size_value = size_s.css("::attr(value)").extract_first()
                    form_data[size_s.css("::attr(name)").extract_first()] = size_value
                    sku["form-data"] = form_data
                    size_title = skus_size_s.css(f"[for*='{size_value}'] >::text").extract_first()
                    sku["size"] = f"{sku['size']}/{size_title}" if sku.get("size") else size_title
                    raw_skus.append(sku)

        return raw_skus
