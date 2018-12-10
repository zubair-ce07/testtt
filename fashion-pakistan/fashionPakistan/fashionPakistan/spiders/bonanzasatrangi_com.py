# -*- coding: utf-8 -*-
import re
import json
import scrapy
from fashionPakistan.items import FashionPakistan


class BonanzasatrangiComSpider(scrapy.Spider):
    name = 'bonanzasatrangi.com'
    start_urls = ['https://www.bonanzasatrangi.com/pk/']

    def parse(self, response):
        category_links = response.xpath(
            "//a[contains(@class, 'shop-all')]/@href").extract()
        for link in category_links:
            yield scrapy.Request(link, self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[contains(@class, 'product-item-photo')]/@href").extract()
        for link in product_links:
            yield scrapy.Request(link, self.parse_product_details)

        next_link = response.xpath("//a[@title='Next']/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, self.parse_product_links)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = response.xpath("//div[@class='product-name']/span/text()").extract_first().strip()
        product["product_sku"] = response.xpath("//div[@itemprop='sku']/text()").extract_first()
        product["description"] = response.xpath("//div[contains(@class, 'description')]/div/p/text()").extract()
        product["images"] = self.get_item_images(response)
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = self.is_in_stock(response)
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def is_in_stock(self, response):
        stock = response.xpath("//div[@title='Availability']/span/text()").extract_first().strip()
        return False if stock == "In stock" else True

    def get_item_attributes(self, response):
        attrib = response.xpath(
            "//div[@class='fabric']/p/text()").extract_first()
        attributes = {}
        if attrib:
            attributes["Fabric"] = attrib.strip()
        return attributes

    def get_item_images(self, response):
        name = response.xpath(
            "//div[@class='product-name']/span/text()").extract_first().strip()
        image_xpath = '//img[contains(@alt, "{}")]/@src'.format(name)
        images = response.xpath(image_xpath).extract()
        return images

    def get_item_sizes(self, response):
        size_string = re.findall(
            r'jsonConfig\":\s+(.+?),\"productId\"', response.text)
        sizes, prices = [], []
        if size_string:
            size_string = size_string[0].strip()
            size_string = size_string+"}"
            json_string = json.loads(size_string)
            for option in json_string["attributes"]["137"]["options"]:
                if option["products"]:
                    sizes.append(option["label"])
                    prices.append(
                        json_string["optionPrices"][option["products"][0]])

        return sizes, prices

    def get_item_skus(self, response):
        color_name = response.xpath(
            "//div[@class='color']/p/text()").extract_first()
        if not(color_name):
            color_name = "no_color"
        currency_code = response.xpath(
            "//meta[@itemprop='priceCurrency']/@content").extract_first()
        price = response.xpath(
            "//span[contains(@id, 'product-price-')]/span[@class='price']/text()").extract_first()
        if price:
            price = price.strip().strip(currency_code)
        prev_price = response.xpath(
            "//span[contains(@id, 'product-price-')]/span[@class='old-price']/span/@data-price-amount").extract_first()
        sizes, prices = self.get_item_sizes(response)
        color_scheme = {}
        if sizes:
            for size, amount in zip(sizes, prices):
                color_scheme[color_name+"_"+size] = {
                    "new_price": amount["finalPrice"]["amount"],
                    "size": size,
                    "currency_code": currency_code
                }
                if prev_price:
                    color_scheme[color_name+"_"+size]["prev_price"] = amount["oldPrice"]["amount"]
        else:
            color_scheme[color_name] = {
                "new_price": price.replace(",", ''),
                "currency_code": currency_code
            }
            if prev_price:
                color_scheme[color_name]["prev_price"] = prev_price.strip(currency_code).strip().replace(",", '')
        return color_scheme
