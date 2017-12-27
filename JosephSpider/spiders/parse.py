from urllib.parse import urlparse

import scrapy

from JosephSpider.spiders.mixin import Mixin


class ParseSpider(scrapy.Spider):
    name = 'item_spider'
    mixin = Mixin()
    allowed_domains = mixin.allowed_domains
    start_urls = mixin.start_urls

    def parse(self, response):
        product = response.meta.get('product') or dict()
        trail = response.meta.get('trail', list())
        trail.append(response.url)

        product["category"] = self.category(response)
        product["gender"] = self.gender(response)
        product["description"] = self.descriptions(response)
        product["care"] = self.cares(response)
        product["retailer_sku"] = self.retailer(response)
        product["image_urls"] = self.images(response)
        product["name"] = self.item_name(response)
        product["brand"] = self.brand(response)
        product["market"] = "US"
        product["retailer"] = "joseph-us"
        product["url"] = response.url

        return self.skus_requests(response, product)

    def parse_color(self, response):
        product = response.meta.get("product")
        skus = product["skus"]
        trail = response.meta["trail"]
        trail.append(response.url)
        remaining_colors = response.meta.get("remaining-colors")
        skus.update(self.product_skus(response))

        if remaining_colors:
            return self.next_requests(response, remaining_colors)
        else:
            return product

    def gender(self, response):
        parent_url = response.meta.get('trail')[0]
        return "women" if "women" in parent_url else "men"

    def category(self, response):

        parent_url = response.meta.get('trail')[1]
        return urlparse(parent_url).path.split('/')[-2]

    def descriptions(self, response):
        descriptions_xpath = "//div[./label[@for='tab-1']]/div[@class='tab-content']/text()"
        return response.xpath(descriptions_xpath).extract()

    def cares(self, response):
        care_xpath = "//div[./label[@for='tab-2']]/div[@class='tab-content']/text()"
        return response.xpath(care_xpath).extract()

    def retailer(self, response):
        retailer_sku = "//meta[@itemprop='SKU']/@content"
        return response.xpath(retailer_sku).extract_first()

    def images(self, response):
        images_xpath = "//div[@id='thumbnails']//img/@src"
        return response.xpath(images_xpath).extract()

    def item_name(self, response):
        name_xpath = "//h1[@itemprop='name']/text()"
        return response.xpath(name_xpath).extract_first()

    def brand(self, response):
        brand_xpath = "//meta[@itemprop='brand']/@content"
        return response.xpath(brand_xpath).extract_first()

    def price(self, response):
        price = response.xpath("//meta[@itemprop='og:price:amount']/@content")
        if price.extract_first():
            return price.extract_first()
        else:
            price = response.xpath("//meta[@itemprop='price']/@content")
            return price.extract_first()

    def currency(self, response):
        currency = response.xpath(
            "//meta[@itemprop='og:price:currency']/@content")
        if currency.extract_first():
            return currency.extract_first()
        else:
            currency = response.xpath(
                "//meta[@itemprop='priceCurrency']/@content")
            return currency.extract_first()

    def color(self, response):
        color = "//ul[contains(@class, 'color')]//li[contains(@class, 'selected')]//img/@alt"
        return response.xpath(color).extract_first()

    def size(self, response):
        size = response.xpath(".//a/@title")
        return size.extract_first().strip("Select Size: ")

    def skus_requests(self, response, product):

        product["skus"] = {}
        colors = response.xpath("//ul[contains(@class, 'color')]//a")
        color = colors.pop()
        request = response.follow(
            color, self.parse_color)
        request.meta["product"] = product
        request.meta["trail"] = response.meta.get("trail")
        request.meta["remaining-colors"] = colors
        yield request

    def next_requests(self, response, remaining_colors):
        color = remaining_colors.pop()
        request = response.follow(
            color, self.parse_color)
        request.meta["product"] = response.meta.get('product')
        request.meta["trail"] = response.meta.get('trail')
        request.meta["remaining-colors"] = remaining_colors
        yield request

    def product_skus(self, response):
        products = dict()
        product = response.meta["product"]
        sizes = response.xpath(
            "//ul[contains(@class, 'size')]//li")
        for size in sizes:
            details = dict()
            details["price"] = self.price(response)
            details["currency"] = self.currency(response)
            details["colour"] = self.color(response)
            details["size"] = self.size(size)

            if size.xpath("self::node()[contains(@class, 'unselectable')]"):
                details["out_of_stock"] = True

            item_key = f'{details["colour"]}_{details["size"]}'
            products[item_key] = details

        return products
