import time

from scrapy import Spider, Request
from w3lib.url import urljoin

from ..items import ProductItem


class ProductParser(Spider):
    name = "forever-new-product-parser"
    currency = "AUD"
    image_base_url = "https://www.forevernew.com.au/balance_superptype/product/media/pid/"

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
        return self.prepare_request(image_requests, product)

    def parse_images(self, response):
        product = response.meta["product"]
        product["image_urls"] += response.css("img.gallery__image::attr('src')").extract()
        return self.prepare_request(response.meta["image_requests"], product)

    def prepare_request(self, requests, product):

        if requests:
            request = requests.pop()
            request.meta["product"] = product
            request.meta["image_requests"] = requests
            yield request
        else:
            yield product

    def raw_skus(self, response):
        colors_s = response.css("#colour-select option:not([availability='0'])")

        raw_skus = {}
        for color in colors_s:
            color_id = color.css("::attr('value')").extract_first()
            sku = {
                "colour": color.css("::attr('label')").extract_first().replace("Colour: ", ""),
                "sizes": response.css(f"li[pid='{color_id}'] option"),
                "price": response.css(f".price-wrapper[pid='{color_id}']")
            }

            if not sku["price"]:
                sku["price"] = response.css(".product-main-info .price-box")

            raw_skus[color_id] = sku

        return raw_skus

    def skus(self, response):
        price_css = ".regular-price .price:not([id])::text, .special-price .price:not([id])::text"
        prev_price_css = ".old-price .price:not([id])::text"
        raw_skus = self.raw_skus(response)
        skus = {}
        common_sku = {"currency": self.currency}

        for sku_id, raw_sku in raw_skus.items():
            sku = common_sku.copy()
            sku["price"] = float(raw_sku['price'].css(price_css).extract_first().strip("$ \n"))
            sku["colour"] = raw_sku["colour"]
            prev_price = raw_sku["price"].css(prev_price_css).extract()

            if prev_price:
                sku["previous_prices"] = [float(price.strip("$ \n")) for price in prev_price]

            if not raw_sku["sizes"]:
                sku["size"] = "One Size"
                skus[sku_id] = sku

            for size_s in raw_sku["sizes"]:
                size_sku = sku.copy()
                size_sku["size"] = size_s.css("::text").extract_first().split(": ")[1].strip().split(" (")[0]

                if size_s.css(".out-of-stock"):
                    size_sku["out-of-stock"] = True

                skus[f"{sku_id}_{size_sku['size']}"] = size_sku

        return skus

    def product_name(self, response):
        return response.css(".product-main-info .product-name h1::text").extract_first()

    def product_id(self, response):
        return response.css(".product-sku::text").extract_first().split("#")[1]

    def price(self, response):
        price_css = (".product-main-info .regular-price .price:not([id])::text"
                     ",.product-main-info .special-price .price:not([id])::text")
        return float(response.css(price_css).extract_first().strip("$ \n"))

    def image_requests(self, response):
        color_ids = response.css("#colour-select option::attr('value')").extract()
        requests = []

        for color_id in color_ids:
            url = urljoin(self.image_base_url, color_id)
            request = Request(url, callback=self.parse_images)
            requests.append(request)

        return requests

    def care(self, response):
        return list(filter(lambda care: care.strip(),
                    response.css(".accordion-container .accordion-content:nth-child(2) li::text").extract()))

    def description(self, response):
        return response.css(".accordion-container .accordion-content:nth-child(2) p::text").extract()

    def category(self, response):
        return response.css(".breadcrumbs span::text").extract()
