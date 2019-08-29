# -*- coding: utf-8 -*-
import re
import itertools

from scrapy import Spider, Request
from scrapy.selector import Selector

from ..items import Product

class AmericangolfParser(Spider):
    name = 'americangolf_parser'
    allowed_domains = ['americangolf.co.uk']
    start_urls = ['https://www.americangolf.co.uk/gps-bags-equipment/trolley-cart-bags/taylormade-deluxe-cart-bag-327073.html?dwvar_327073_variantimage=black%2Forange']
    possible_genders = ['Female', 'Male', 'Unisex']

    def parse(self, response):
        product_item = Product()
        product_item['name'] = self.product_name(response)
        product_item['retailer_sku'] = self.product_retailer_sku(response)
        product_item['brand'] = self.product_brand(response)
        product_item['lang'] = self.product_lang(response)
        product_item['description'] = self.product_description(response)
        product_item['care'] = self.product_care(response)
        product_item['image_urls'] = self.product_image_urls(response)
        product_item['gender'] = self.product_gender(response)
        product_item['category'] = self.product_categories(response)
        product_item['url'] = response.url
        product_item['skus'] = {}

        sku_requests = self.get_color_skus_requests(response)
        sku_requests += self.get_varients_skus_requests(response)
        if sku_requests:
            product_item['meta'] = {'request_queue': sku_requests}
            return self.yield_next_request_or_item(product_item)

        product_item['skus'] = self.varient_sku(response)
        return product_item

    def parse_colour_skus(self, response):
        product_item = response.meta['product_item']
        product_item['skus'].update(self.color_skus(response))
        return self.yield_next_request_or_item(product_item)

    def parse_hardware_skus(self, response):
        product_item = response.meta['product_item']
        sku_requests = self.get_varients_skus_requests(response)
        if sku_requests:
            product_item['meta']['request_queue'] += sku_requests
        else:
            product_item['skus'].update(self.varient_sku(response))

        return self.yield_next_request_or_item(product_item)

    def varient_sku(self, response):
        raw_varients = response.css(".product-variations .attribute").getall()
        varient_titles = []
        varient_values = []
        for varient in raw_varients:
            selector = Selector(text=varient)
            varient_titles.append(selector.css(".variation-select::attr(data-variationattribute)").get())
            varient_values.append(
                selector.css(".variation-select option[selected='selected']::attr(data-variationvalue)").get())

        product_price = self.product_price(response)
        previous_prices = self.product_previous_prices(response)
        currency = self.product_currency(response)
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

    def product_name(self, response):
        return response.css('.pdp-top .product-name::text').get().strip()

    def product_retailer_sku(self, response):
        return response.css('.product-info .product-code span::text').get()

    def product_brand(self, response):
        return response.css(".pdp-top .product-brand img::attr(alt)").get()
    
    def product_lang(self, response):
        return response.css('html::attr(lang)').get()

    def product_description(self, response):
        description = response.css(".product-info .product-detaildescription .paragraph::text").getall()
        return list(filter(None, map(str.strip, description)))

    def product_care(self, response):
        care = response.css(".product-info .bullet-list li::text").getall()
        return list(filter(None, map(str.strip, care)))
    
    def product_image_urls(self, response):
        image_links = response.css('.pdp-top .product-images .carousel-tile a::attr(href)').getall()
        primary_images = response.css('.pdp-top .product-primary-image img::attr(data-src)').getall()
        return image_links or primary_images
    
    def product_gender(self, response):
        soup = re.findall('var google_tag_params =(.+?);\n', response.body.decode("utf-8"), re.MULTILINE | re.DOTALL)[0]
        for gender in self.possible_genders:
            if gender.lower() in soup.lower():
                return gender
    
    def product_categories(self, response):
        return response.css('.pdp-breadcrumb-bar .breadcrumb-element a::text').getall()[1:]

    def product_price(self, response):
        return response.css(".pdp-top .product-sales-price::attr(content)").get()
    
    def product_previous_prices(self, response):
        return response.css(".pdp-top .mrrp .value::text").getall()

    def product_currency(self, response):
        return response.css(".pdp-top .product-price-container span::text").get()
    
    def get_color_skus_requests(self, response):
        urls = response.css(".product-variations .swatches-color a::attr(data-select-url)").getall()
        requests = [Request(url, callback=self.parse_colour_skus) for url in urls]
        return requests

    def color_skus(self, response):
        product_price = self.product_price(response)
        previous_prices = self.product_previous_prices(response)
        currency = self.product_currency(response)
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

        return colour_skus

    def get_varients_skus_requests(self, response):
        urls = response.css(".product-variations .attribute.variant-hardware.pleaseselect option::attr(value)").getall()
        requests = [Request(url, callback=self.parse_hardware_skus) for url in urls if url]
        return requests

    def yield_next_request_or_item(self, product_item):
        if product_item['meta'] and product_item['meta']['request_queue']:
            request = product_item['meta']['request_queue'].pop()
            request.meta['product_item'] = product_item
            return request

        del product_item['meta']
        return product_item
