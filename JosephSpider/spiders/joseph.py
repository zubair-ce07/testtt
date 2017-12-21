# -*- coding: utf-8 -*-
import sys
from urllib.parse import urlparse
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.    spiders import CrawlSpider, Rule


class JosephSpider(CrawlSpider):
    name = "joseph_spider"
    allowed_domains = ['joseph-fashion.com']
    start_urls = ["http://www.joseph-fashion.com/en-us/home"]

    rules = (
        Rule(LinkExtractor(
            restrict_css='a[class*="navigation__link"]')),
        Rule(LinkExtractor(restrict_css='.search-result-content .thumb-link'),
             callback='parse_product'),
    )

    def parse_product(self, response):
        data = {}

        brand = response.xpath("//meta[@itemprop='brand']/@content")
        data["brand"] = brand.extract_first()
        data["market"] = "US"
        data["retailer"] = "joseph-us"
        name = response.xpath("//h1[@itemprop='name']/text()")
        data["name"] = name.extract_first()
        data["care"] = self.parse_care(response)
        data["description"] = self.parse_description(response)
        data["image_urls"] = self.parse_images(response)
        retailer_sku = response.xpath("//meta[@itemprop='SKU']/@content")
        data["retailer_sku"] = retailer_sku.extract_first()
        data["url"] = response.url
        referrer = str(response.request.headers.get('Referer'))
        data["gender"] = self.parse_gender(response)
        data["category"] = urlparse(referrer).path.split('/')[-2]
        return self.parse_skus(response, data)

    def parse_gender(self, response):
        referer_link = response.request.headers.get("Referer")
        return "women" if b"women" in referer_link else "men"

    def parse_care(self, response):
        cares = response.xpath(
            "//div[./label[@for='tab-2']]/div[@class='tab-content']/text()")
        return [care.extract() for care in cares]

    def parse_images(self, response):
        images = response.xpath("//div[@id='thumbnails']//img/@src")
        return [image_url.extract() for image_url in images]

    def parse_description(self, response):
        descriptions = response.xpath(
            "//div[./label[@for='tab-1']]/div[@class='tab-content']/text()")
        return [description.extract() for description in descriptions]

    def parse_skus(self, response, data):

        data["skus"] = {}
        colors = response.xpath("//ul[contains(@class, 'color')]//a")
        for color in colors:
            request = response.follow(
                color, self.parse_skus_callback)
            request.meta["product"] = data
            yield request
        return data

    def parse_skus_callback(self, response):

        data = response.meta["product"]
        data_catalogue = data["skus"]
        data_catalogue.update(self.parse_in_stock(response))
        data_catalogue.update(self.parse_out_of_stock(response))
        return data

    def parse_in_stock(self, response):
        items = dict()
        data = response.meta["product"]
        selectable = response.xpath(
            "//ul[contains(@class, 'size')]//li[contains(@class, 'selectable')]/a/@title")
        for selectable_size in selectable:
            details = self.parse_size(response, selectable_size)
            details["out_of_stock"] = "False"
            item_key = details["colour"]+"_"+details["size"]
            items[item_key] = details
        return items

    def parse_out_of_stock(self, response):
        items = dict()
        data = response.meta["product"]
        out_stock = response.xpath(
            "//ul[contains(@class, 'size')]//li[contains(@class, 'unselectable')]/a/@title")
        for out_stock_size in out_stock:
            details = self.parse_size(response, out_stock_size)
            details["out_of_stock"] = "False"
            item_key = details["colour"]+"_"+details["size"]
            items[item_key] = details
        return items

    def parse_size(self, response, item):
        details = dict()
        price = response.xpath("//meta[@itemprop='price']/@content")
        currency = response.xpath("//meta[@itemprop='priceCurrency']/@content")
        color = response.xpath(
            "//ul[contains(@class, 'color')]//li[contains(@class, 'selected')]//img/@alt")
        size = item.extract().strip("Select Size: ")
        details["colour"] = color.extract_first()
        details["currency"] = currency.extract_first()
        details["price"] = price.extract_first()
        details["size"] = size
        return details
