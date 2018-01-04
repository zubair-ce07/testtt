from urllib.parse import urlparse

import scrapy

from JosephSpider.spiders.mixin import Mixin


class ParseSpider(scrapy.Spider, Mixin):
    name = 'item_spider'

    def parse(self, response):
        product = response.meta.get('product') or dict()
        product["category"] = self.category(product)
        product["gender"] = self.gender(product)
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
        skus = product.get("skus")
        trail = product.get("trail")
        remaining_colors = product.get("remaining-colors")
        skus.update(self.skus(response))

        if remaining_colors:
            return self.next_requests(response, remaining_colors)
        else:
            return product

    def gender(self, product):
        parent_url = product.get('trail')[0]
        return "women" if "women" in parent_url else "men"

    def category(self, product):

        parent_url = product.get('trail')[0]
        return urlparse(parent_url).path.split('/')[-1]

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
        response.meta["product"] = product
        remaining_colors = response.xpath("//ul[contains(@class, 'color')]//a")
        return self.next_requests(response, remaining_colors)

    def next_requests(self, response, remaining_colors):
        product = response.meta.get('product')
        color = remaining_colors.pop()
        product["remaining-colors"] = remaining_colors
        request = response.follow(
            color, self.parse_color)
        request.meta["product"] = response.meta.get('product')
        yield request

    def skus(self, response):
        products = dict()
        skus = response.xpath(
            "//ul[contains(@class, 'size')]//li")
        for sku in skus:
            details = dict()
            details["price"] = self.price(response)
            details["currency"] = self.currency(response)
            details["colour"] = self.color(response)
            details["size"] = self.size(sku)

            if sku.xpath("self::node()[contains(@class, 'unselectable')]"):
                details["out_of_stock"] = True

            item_key = f'{details["colour"]}_{details["size"]}'
            products[item_key] = details

        return products
