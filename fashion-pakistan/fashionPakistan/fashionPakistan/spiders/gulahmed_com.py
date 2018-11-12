# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan

class GulahmedComSpider(scrapy.Spider):
    name = 'gulahmed.com'
    start_urls = ['https://www.gulahmedshop.com']

    def parse(self, response):
        category_links = response.xpath("//a[@class='menu-link']/@href").extract()[:-1]
        for link in category_links:
            yield scrapy.Request(link+"?product_list_limit=100", self.parse_products)

    def parse_products(self, response):
        product_links = response.xpath("//a[contains(@class, 'product-item-photo')]/@href").extract()
        for link in product_links:
            yield scrapy.Request(link, self.parse_item_details)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = self.get_item_name(response)
        product["product_sku"] = self.get_item_sku(response)
        product["description"] = self.get_item_description(response)
        product["images"] = self.get_item_images(response)
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = False
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def get_item_name(self, response):
        return response.xpath("//span[@data-ui-id]/text()").extract_first()

    def get_item_sku(self, response):
        return response.xpath("//div[@itemprop='sku']/text()").extract_first()

    def get_item_description(self, response):
        return response.xpath("//div[@itemprop='description']//text()").extract()

    def get_item_images(self, response):
        images = response.xpath(
            "//img[@class='fotorama__img']/@src").extract()
        images = images[:int(len(images)/2)]
        return images

    def get_item_sizes(self, response):
        size_string = re.findall(r'swatchOptions\":[\W\w]*},\"tierPrices\":\[\]}},|$',response.text)[0]
        size_string = size_string.strip("swatchOptions\":")
        size_string = size_string.strip(",")
        size_string = size_string+"}"
        sizes = []
        prices = []
        if size_string != "}":
            json_string = json.loads(size_string)
            for option in json_string["attributes"]["142"]["options"]:
                sizes.append(option["label"])
                prices.append(json_string["optionPrices"][option["products"][0]]["finalPrice"]["amount"])

        return sizes, prices

    def get_item_skus(self, response):
        color_name = response.xpath(
            "//td[@data-th='Color']/text()").extract_first()
        price = response.xpath("//span[@class='price']/text()").extract_first()
        currency = response.xpath(
            "//meta[@itemprop='priceCurrency']/@content").extract_first()
        sizes, prices = self.get_item_sizes(response)
        color_scheme = {}
        if sizes:
            for size, amount in zip(sizes, prices):
                color_scheme[color_name+"_"+size] = {
                    "color": color_name,
                    "price": amount,
                    "size": size,
                    "currency_code": currency,
                }
        else:
            color_scheme[color_name] = {
                "color": color_name,
                "price": price,
                "currency_code": currency,
            }
        return color_scheme
