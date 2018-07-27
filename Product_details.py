import requests
import re
from parsel import Selector


class Sku(object):
    def __init__(self):
        self.color = ""
        self.price = ""
        self.currency = ""
        self.size = ""
        self.previous_prices = []
        self.out_of_stock = "false"
        self.sku_id = ""

    def extract_sku_features(self, selector, size, retailer_sku):
        self.color = selector.css('.color::text').get()

        self.price = selector.css(
            '[id^=product-price] > .price::text').get()

        self.currency = selector.css(
            '.inner-heading > .label::text').getall()[1]

        self.size = size

        old_price = selector.css(
            '[id^=old-price] > .price::text').get()

        self.previous_prices.append(old_price)

        self.sku_id = retailer_sku + "_" + size

        return self.__dict__


class Product(object):
    def __init__(self, url):

        self.retailer_sku = ""
        self.gender = 'women' if 'women' in url else 'men'
        self.category = []
        self.brand = "The Upside Sport"
        self.url = url
        self.name = ""
        self.description = ""
        self.care = ""
        self.image_urls = []
        self.skus = []

    def extract_category(self):

        category = re.search(
            r'^https:\/\/[^\/]*\/[^\/]*\/[^\/]*\/([^\/]*).*', self.url)

        if category:
            return "sale" if "sale" in self.url else category.group(1)
        else:
            return ""

    def extract_image_urls(self, selector):

        images_script = selector.xpath(
            '//script[@type="text/x-magento-init" and contains(text(), "mage/gallery/gallery")]/text()').get()

        images = re.findall(
            r'\"full\":\"https:[\\/a-z0-9\.\-_]+\.png', images_script)

        return [img.replace('\\', '').replace(
            '\"full\":\"', '') for img in images]

    def extract_sizes(self, selector):

        sizes_script = selector.xpath(
            '//script[contains(text(), "AEC.SUPER")]/text()').get()
        sizes = re.findall('\"default_label\": \"(.+?)\",', sizes_script)

        return sizes

    def parse_product(self):
        selector = Selector(requests.get(self.url).text)

        self.retailer_sku = selector.css(
            '.product.attribute.sku.custom > .value::text').get()

        self.category = self.extract_category()

        self.name = selector.css('.page-title > .base::text').get()

        self.description = selector.css(
            '.product.attribute.description > .value > .p1::text').getall()

        self.care = selector.css('.fabric-care > ul > li::text').getall()

        self.image_urls = self.extract_image_urls(selector)

        sizes = self.extract_sizes(selector)

        for size in sizes:

            sku = Sku().extract_sku_features(selector, size, self.retailer_sku)

            self.skus.append(sku)

        return self.__dict__
