import time

from scrapy import Spider, Request
from w3lib.url import urljoin

from ..items import ProductItem


class ProductParser(Spider):
    name = "forever-new-product-parser"
    currency = "AUD"
    start_urls = ["https://www.forevernew.com.au/grace-7-8th-slim-pants-228316"]

    def parse(self, response):
        product = ProductItem()
        product["retailer_sku"] = self.product_id(response)
        product["lang"] = "en"
        product["trail"] = response.meta.get("trail", [])
        product["gender"] = "women"
        product["category"] = self.category(response)
        product["brand"] = "Forever New"
        product["url"] = response.url
        product["date"] = int(time.time())
        product["market"] = "AU"
        product["url_original"] = response.url
        product["name"] = self.product_name(response)
        product["description"] = self.description(response)
        product["care"] = self.care(response)
        product["skus"] = self.skus(response)

        if product["skus"]:
            product["price"] = self.price(response)
            product["currency"] = self.currency
        else:
            product["out_of_stock"] = True

        product["image_urls"] = []
        image_requests = self.image_requests(response)
        request = image_requests.pop()
        request.meta["product"] = product
        request.meta["image_requests"] = image_requests
        yield request

    def skus_map(self, response):
        colors = response.css("#colour-select option")

        sku_map = {}
        for color in colors:

            if color.css("::attr('availability')").extract_first() == "0":
                continue

            color_id = color.css("::attr('value')").extract_first()
            sku = {
                "color": color.css("::attr('label')").re_first(":\s(.+)"),
                "sizes": response.css(f"li[pid='{color_id}'] option"),
                "price": response.css(f".price-wrapper[pid='{color_id}']")
            }

            if not sku["price"]:
                sku["price"] = response.css(".product-main-info .price-box")

            sku_map[color_id] = sku

        return sku_map

    def skus(self, response):
        price_css = ".regular-price .price,.special-price .price"
        prev_price_css = ".old-price .price:not([id])"
        price_re = "\\$(\d+.\d+)"
        sku_map = self.skus_map(response)

        skus = {}
        common_sku = {"currency": self.currency}
        for sku_id, raw_sku in sku_map.items():
            sku = common_sku.copy()
            sku["price"] = float(raw_sku['price'].css(price_css).re_first(price_re))
            sku["color"] = raw_sku["color"]
            prev_price = raw_sku["price"].css(prev_price_css).re(price_re)

            if prev_price:
                sku["previous_prices"] = [float(price) for price in prev_price]

            if not raw_sku["sizes"]:
                sku["size"] = "unisize"
                skus[sku_id] = sku.copy()
                continue

            for size in raw_sku["sizes"]:

                if size.css("::attr('class')").extract_first() == "out-of-stock":
                    continue

                product_id = size.css("::attr('pid')").extract_first()
                sku["size"] = size.css("::text").re_first(".*:\s([\w-]*)\s")
                skus[product_id] = sku.copy()

        return skus

    def product_name(self, response):
        return response.css(".product-main-info .product-name h1::text").extract_first()

    def product_id(self, response):
        return response.css(".product-sku::text").re_first("#(\w+)")

    def price(self, response):
        price_css = (".product-main-info .price-box .regular-price .price"
                     ",.product-main-info .price-box .special-price .price")
        price_re = "\\$(\d+.\d+)"
        return float(response.css(price_css).re_first(price_re))

    def image_requests(self, response):
        color_ids = response.css("#colour-select option::attr('value')").extract()
        request_url = "https://www.forevernew.com.au/balance_superptype/product/media/pid/"
        requests = []

        for color_id in color_ids:
            url = urljoin(request_url, color_id)
            request = Request(url, callback=self.parse_images)
            requests.append(request)

        return requests

    def parse_images(self, response):
        product = response.meta["product"]
        product["image_urls"].extend(response.css("img.gallery__image::attr('src')").extract())

        if not response.meta["image_requests"]:
            yield product
        else:
            request = response.meta["image_requests"].pop()
            request.meta["product"] = product
            request.meta["image_requests"] = response.meta["image_requests"]
            yield request

    def care(self, response):
        return response.css(".accordion-container .accordion-content:nth-child(2) li::text").re("\S.*")

    def description(self, response):
        return response.css(".accordion-container .accordion-content:nth-child(2) p::text").extract()

    def category(self, response):
        return response.css(".breadcrumbs span::text").extract()
