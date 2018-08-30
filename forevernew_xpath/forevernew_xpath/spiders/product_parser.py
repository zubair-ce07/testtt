import time

from scrapy import Spider, Request
from w3lib.url import urljoin

from ..items import ProductItem


class ProductParser(Spider):
    name = "forever-new-product-parser"
    currency = "AUD"
    image_base_url = "https://www.forevernew.com.au/balance_superptype/product/media/pid/"
    seen_skus = set()

    def parse(self, response):
        product = ProductItem()
        retailer_sku = self.product_id(response)

        if retailer_sku in self.seen_skus:
            return

        self.seen_skus.add(retailer_sku)
        product["retailer_sku"] = retailer_sku
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
        product["image_urls"] += self.image_urls(response)
        return self.prepare_request(response.meta["image_requests"], product)

    def image_urls(self, response):
        return response.xpath("//img[@class='gallery__image']/@src").extract()

    def prepare_request(self, requests, product):

        if requests:
            request = requests.pop()
            request.meta["product"] = product
            request.meta["image_requests"] = requests
            yield request
        else:
            yield product

    def raw_skus(self, response):
        colors_s = response.xpath("//*[@id='colour-select']/option[not(@availability='0')]")

        raw_skus = {}
        for color in colors_s:
            color_id = color.xpath("@value").extract_first()
            sku = {
                "colour": color.xpath("@label").extract_first().replace("Colour: ", ""),
                "sizes": response.xpath(f"//li[@pid='{color_id}']//option"),
                "price": response.xpath(f"//*[@class='price-wrapper' and @pid='{color_id}']")

            }

            if not sku["price"]:
                sku["price"] = response.xpath("//div[@class='product-main-info']/div[@class='price-box']")

            raw_skus[color_id] = sku

        return raw_skus

    def skus(self, response):
        price_xpath = ("*[@class='regular-price' or @class='special-price']"
                       "//span[@class='price' and contains(text(), '$')]/text()")
        prev_price_xpath = "*[@class='old-price']//*[@class='price' and contains(text(), '$')]/text()"
        raw_skus = self.raw_skus(response)
        skus = {}
        common_sku = {"currency": self.currency}

        for sku_id, raw_sku in raw_skus.items():
            sku = common_sku.copy()
            sku["price"] = float(raw_sku['price'].xpath(price_xpath).extract_first().strip("$ \n"))
            sku["colour"] = raw_sku["colour"]
            prev_price = raw_sku["price"].xpath(prev_price_xpath).extract()

            if prev_price:
                sku["previous_prices"] = [float(price.strip("$ \n")) for price in prev_price]

            if not raw_sku["sizes"]:
                sku["size"] = "One Size"
                skus[sku_id] = sku

            for size_s in raw_sku["sizes"]:
                size_sku = sku.copy()
                size_sku["size"] = size_s.xpath("text()").extract_first().split(": ")[1].strip().split(" (")[0]

                if size_s.xpath("@class='out-of-stock'").extract_first() == '1':
                    size_sku["out-of-stock"] = True

                skus[f"{sku_id}_{size_sku['size']}"] = size_sku

        return skus

    def product_name(self, response):
        return response.xpath("//*[@class='product-main-info']//*[@class='product-name']/h1/text()").extract_first()

    def product_id(self, response):
        return response.xpath("//*[@class='product-sku']/text()").extract_first().split("#")[1]

    def price(self, response):
        price_xpath = ("//*[@class='product-main-info']//*[@class='regular-price' or @class='special-price']//"
                       "*[@class='price' and contains(text(), '$')]/text()")
        return float(response.xpath(price_xpath).extract_first().strip("$ \n"))

    def image_requests(self, response):
        color_ids = response.xpath("//*[@id='colour-select']//option/@value").extract()
        requests = []

        for color_id in color_ids:
            url = urljoin(self.image_base_url, color_id)
            request = Request(url, callback=self.parse_images)
            requests.append(request)

        return requests

    def care(self, response):
        care_xpath = "//*[@class='accordion-container']//*[@class='accordion-content'][1]//li/text()"
        return [care for care in response.xpath(care_xpath).extract() if care.strip()]

    def description(self, response):
        return response.xpath("//*[@class='accordion-container']//*[@class='accordion-content'][1]//p/text()").extract()

    def category(self, response):
        return response.xpath("//*[@class='breadcrumbs']//span/text()").extract()
