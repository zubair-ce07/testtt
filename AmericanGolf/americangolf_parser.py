# -*- coding: utf-8 -*-
import re
import itertools

from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import Product

class AmericangolfParser(Spider):
    name = 'americangolf_parser'
    allowed_domains = ['americangolf.co.uk']
    start_urls = ['http://americangolf.co.uk/']
    possible_genders = ['Female', 'Male', 'Unisex']

    def parse(self, response):
        return self.parse_product(response)

    def parse_product(self, response):
        product_item = Product()
        product_item['name'] = response.css('.pdp-top .product-name::text').get().strip()
        product_item['retailer_sku'] = response.css('.product-info .product-code span::text').get()
        product_item['brand'] = response.css(".pdp-top .product-brand img::attr(alt)").get()
        product_item['lang'] = response.css('html::attr(lang)').get()
        product_item['description'] = self.parse_description(response)
        product_item['care'] = self.parse_care(response)
        product_item['image_urls'] = self.parse_image_urls(response)
        product_item['url'] = response.request.url
        product_item['gender'] = self.parse_gender(response)
        product_item['category'] = self.parse_categories(response)
        product_item['skus'] = {}

        return self.handle_skus(response, product_item)

    def parse_description(self, response):
        description = response.css(".product-info .product-detaildescription .paragraph::text").getall()
        return list(filter(None, map(str.strip, description)))

    def parse_care(self, response):
        care = response.css(".product-info .bullet-list li::text").getall()
        return list(filter(None, map(str.strip, care)))
    
    def parse_image_urls(self, response):
        image_links = response.css('.pdp-top .product-images .carousel-tile a::attr(href)').getall()
        primary_images = response.css('.pdp-top .product-primary-image img::attr(data-src)').getall()
        return image_links or primary_images
    
    def parse_gender(self, response):
        soup = re.findall('var google_tag_params =(.+?);\n', response.body.decode("utf-8"), re.MULTILINE | re.DOTALL)[0]
        for gender in self.possible_genders:
            if gender.lower() in soup.lower():
                return gender
    
    def parse_categories(self, response):
        return response.css('.pdp-breadcrumb-bar .breadcrumb-element a::text').getall()[1:]

    def parse_price(self, response):
        return response.css(".pdp-top .product-sales-price::attr(content)").get()
    
    def parse_previous_prices(self, response):
        return response.css(".pdp-top .mrrp .value::text").getall()

    def parse_currency(self, response):
        return response.css(".pdp-top .product-price-container span::text").get()

    def get_color_skus_requests(self, response):
        urls = response.css(".product-variations .swatches-color a::attr(data-select-url)").getall()
        requests = [Request(url, callback=self.parse_colour_skus) for url in urls]
        return requests
    
    def get_varients_skus_requests(self, response):
        urls = response.css(".product-variations .attribute.variant-hardware.pleaseselect option::attr(value)").getall()
        urls = list(filter(None, urls))
        requests = [Request(url, callback=self.parse_hardware_skus) for url in urls]
        return requests

    def handle_skus(self, response, product_item):
        sku_requests = self.get_color_skus_requests(response)
        sku_requests += self.get_varients_skus_requests(response)
        if sku_requests:
            product_item['meta'] = {'request_queue': sku_requests}
            return self.check_sku_requests(product_item)

        product_item['skus'] = self.get_varient_sku(response)
        return product_item

    def parse_hardware_skus(self, response):
        product_item = response.meta['product_item']
        sku_requests = self.get_varients_skus_requests(response)
        if sku_requests:
            product_item['meta']['request_queue'] += sku_requests
        else:
            product_item['skus'].update(self.get_varient_sku(response))
        
        return self.check_sku_requests(product_item)
        
    def parse_colour_skus(self, response):
        product_item = response.meta['product_item']
        product_price = self.parse_price(response)
        previous_prices = self.parse_previous_prices(response)
        currency = self.parse_currency(response)
        product_sizes = response.css(".product-variations .size a::attr(data-variationvalue)").getall()
        selected_colour = response.css(".product-variations .swatches-color .swatch.selected a::attr(data-variationvalue)").get()

        colour_skus = {}
        for size in product_sizes or [1]:
            new_sku = {
                "price": product_price,
                "currency": currency,
                "previous_prices": previous_prices,
                "colour": selected_colour, 
                "size": size
            }
            colour_skus[f"{selected_colour}_{size}"] = new_sku

        product_item['skus'].update(colour_skus)
        return self.check_sku_requests(product_item)

    def check_sku_requests(self, product_item):
        if product_item['meta'] and product_item['meta']['request_queue']:
            request = product_item['meta']['request_queue'].pop()
            request.meta['product_item'] = product_item
            return request

        del product_item['meta']
        return product_item

    def get_varient_sku(self, response):
        raw_varients = response.css(".product-variations .attribute").getall()
        varient_titles = []
        varient_values = []
        for varient in raw_varients:
            selector = Selector(text=varient)
            varient_titles.append(selector.css(".variation-select::attr(data-variationattribute)").get())
            varient_values.append(selector.css(".variation-select option[selected='selected']::attr(data-variationvalue)").get())

        product_price = self.parse_price(response)
        previous_prices = self.parse_previous_prices(response)
        currency = self.parse_currency(response)
        varient_sku = {}
        new_sku = {
                "price": product_price,
                "currency": currency,
                "previous_prices": previous_prices
            }
        for varient, value in zip(varient_titles, varient_values):
            new_sku[varient] = value
        varient_sku['_'.join(varient_values)] = new_sku
        return varient_sku
