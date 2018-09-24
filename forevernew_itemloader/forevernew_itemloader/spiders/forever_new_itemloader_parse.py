from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from w3lib.url import urljoin

from ..items import ProductItem


class ForeverNewItemloaderParseSpider(Spider):
    name = 'forever-new-itemloader-parse'
    image_base_url = "https://www.forevernew.com.au/balance_superptype/product/media/pid/"

    def parse(self, response):
        product_loader = ItemLoader(item=ProductItem(), response=response)
        product_loader.add_css("retailer_sku", ".product-sku::text")
        product_loader.add_value("lang", "en")
        product_loader.add_value("trail", response.meta.get("trail", []))
        product_loader.add_value("gender", "women")
        product_loader.add_css("category", ".breadcrumbs span::text")
        product_loader.add_value("brand", "Forever New")
        product_loader.add_value("url", response.url)
        product_loader.add_value("market", "AU")
        product_loader.add_value("url_original", response.url)
        product_loader.add_css("name", ".product-main-info .product-name h1::text")
        product_loader.add_css("description", ".accordion-container .accordion-content:nth-child(2) p::text")
        product_loader.add_css("care", ".accordion-container .accordion-content:nth-child(2) li::text")
        product_loader.add_value("skus", self.raw_skus(response))
        if product_loader.get_collected_values("skus"):
            product_loader.add_css("price", ".product-main-info .regular-price .price:not([id])::text"
                                   ",.product-main-info .special-price .price:not([id])::text")
            product_loader.add_value("currency", "USD")
        else:
            product_loader.add_value("out_of_stock", True)

        return self.prepare_request(self.image_requests(response), product_loader)

    def parse_images(self, response):
        il = response.meta["product_loader"]
        il.add_css("image_urls", "img.gallery__image::attr('src')")
        return self.prepare_request(response.meta["image_requests"], il)

    def image_requests(self, response):
        color_ids = response.css("#colour-select option::attr('value')").extract()
        requests = []

        for color_id in color_ids:
            url = urljoin(self.image_base_url, color_id)
            request = Request(url, callback=self.parse_images)
            requests.append(request)

        return requests

    @staticmethod
    def prepare_request(requests, product_loader):

        if requests:
            request = requests.pop()
            request.meta["product_loader"] = product_loader
            request.meta["image_requests"] = requests
            yield request
        else:
            yield product_loader.load_item()

    @staticmethod
    def raw_skus(response):
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
