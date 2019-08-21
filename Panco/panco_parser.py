# -*- coding: utf-8 -*-
import json
from urllib import parse

from scrapy import Spider, Request
import w3lib.url

from ..items import Product

class PancoParserSpider(Spider):
    name = 'panco_parser'
    allowed_domains = ['panco.com']
    start_urls = ['https://www.panco.com.tr']
    possible_genders = ['Yenidoğan', 'Kiz Bebek', 'Kiz Çocuk', 'Erkek Bebek', 'Erkek Çocuk']

    def parse_product(self, response):
        product_item = Product()
        raw_product = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_item['name'] = response.css(".product-name::text").get()
        product_item['retailer_sku'] = response.css(".product-number::text").get()
        product_item['brand'] = raw_product['productDetail']['data']['brand']
        product_item['lang'] = response.css("html::attr(lang)").get()
        product_item['description'] = response.css(".js-product-content__tab--delivery div.content::text").get().strip()
        product_item['image_urls'] = response.css(".js-product-slider__main img::attr(src)").getall()
        product_item['category'] = self.get_category(response)
        product_item['gender'] = self.get_gender(response)
        product_item['url'] = response.request.url
        product_item['skus'] = {}
        product_item['meta'] = {'request_queue': self.get_skus_requests(response)}

        return self.check_sku_requests(product_item)

    def get_category(self, response):
        return response.css(".breadcrumb a::text, .breadcrumb span::text").getall()[1:]

    def get_gender(self, response):
        category = ' '.join(self.get_category(response))
        for gender in self.possible_genders:
            if gender.lower() in category.lower():
                return gender

    def get_skus_requests(self, response):
        colors = response.css(".product-variant__item .variants-wrapper a::attr(data-value)").getall()
        requests = []
        for color in colors:
            url = w3lib.url.add_or_replace_parameter(response.request.url, 'integration_color', color)
            requests.append(Request(url, callback=self.parse_colour_skus))
        return requests

    def check_sku_requests(self, product_item):
        if product_item['meta'] and product_item['meta']['request_queue']:
            request = product_item['meta']['request_queue'].pop(0)
            request.meta['product_item'] = product_item
            return request
        else:
            del product_item['meta']
            return product_item

    def get_selected_colour(self, response):
        return response.css(".product-variant__item .variants-wrapper a.is-select::attr(data-value)").get()

    def parse_colour_skus(self, response):
        product_item = response.meta['product_item']

        raw_product = json.loads(response.css(".js-main-wrapper .analytics-data::text").get())
        product_price = raw_product['productDetail']['data']['price']
        old_prices = [raw_product['productDetail']['data']['dimension16']]
        currency = response.css("head meta[property='og:price:currency']::attr(content)").get()
        product_sizes = response.css(".product-variant__item .product-size-item::attr(data-value)").getall()
        size_availability = self.get_size_availability(response)
        selected_colour = self.get_selected_colour(response)

        colour_skus = {}
        for size, availble in zip(product_sizes, size_availability):
            new_sku = {
                "price": product_price,
                "currency": currency,
                "previous_prices": old_prices,
                "colour": selected_colour, 
                "size": size
            }
            if not availble:
                new_sku['out_of_stock'] = True
            colour_skus[f"{selected_colour}_{size}"] = new_sku
        product_item['skus'].update(colour_skus)
        return self.check_sku_requests(product_item)

    def get_size_availability(self, response):
        size_classes = response.css(".product-variant__item .product-size-item::attr(class)").getall()
        return ["is-disable" not in attr for attr in size_classes]
