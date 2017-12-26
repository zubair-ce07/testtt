from urllib.parse import urlparse

import scrapy

from .mixin import Mixin


class ParseSpider(scrapy.Spider):
    name = 'item_spider'
    mixin = Mixin()
    allowed_domains = mixin.allowed_domains
    start_urls = mixin.start_urls

    def parse(self, response):
        product = response.meta["product"]
        data_catalogue = product["skus"]
        data_catalogue.update(self.item_catalogue(response))
        return product

    def parse_product(self, response):
        data = response.meta.get('data') or dict()
        data['trail'] = data.get('trail') or list()
        data["trail"].append(response.url)
        referrer = data['trail'][0]
        data["category"] = self.category(referrer)
        data["gender"] = self.gender(referrer)     
        data["description"] = self.descriptions(response)
        data["care"] = self.cares(response)
        data["retailer_sku"] = self.retailer(response)
        data["image_urls"] = self.images(response)
        data["name"] = self.item_name(response)
        data["brand"] = self.brand(response)
        data["market"] = "US"
        data["retailer"] = "joseph-us"

        return self.skus_requests(response, data)

    def gender(self, referrer):
        return "women" if "women" in referrer else "men"

    def category(self, referrer):
        return urlparse(referrer).path.split('/')[-2]

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

    def skus_requests(self, response, data):

        data["skus"] = {}
        colors = response.xpath("//ul[contains(@class, 'color')]//a")
        for color in colors:
            request = response.follow(
                color, self.parse)
            request.meta["product"] = data
            yield request

    def item_catalogue(self, response):
        items = dict()
        product = response.meta["product"]
        product["trail"].append(response.url)
        sizes = response.xpath(
            "//ul[contains(@class, 'size')]//li")
        for size in sizes:
            details = self.item_size(response, size)
            if size.xpath("self::node()[contains(@class, 'unselectable')]"):
                details["out_of_stock"] = True

            item_key = f'{details["colour"]}_{details["size"]}'
            items[item_key] = details

        return items

    def item_size(self, response, item):
        details = dict()
        price = response.xpath("//meta[@itemprop='price']/@content")
        currency = response.xpath("//meta[@itemprop='priceCurrency']/@content")
        color = response.xpath(
            "//ul[contains(@class, 'color')]//li[contains(@class, 'selected')]//img/@alt")
        size = item.xpath("//a/@title").extract_first().strip("Select Size: ")
        details["colour"] = color.extract_first()
        details["currency"] = currency.extract_first()
        details["price"] = price.extract_first()
        details["size"] = size
        return details
