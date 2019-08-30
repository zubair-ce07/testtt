# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import Product

class HellyhansenParser(Spider):
    name = 'hellyhansenparser'
    allowed_domains = ['hellyhansen.com']
    start_urls = ['http://hellyhansen.com/en_gb/']
    possible_genders = ['Men', 'Women', 'Kids']

    def parse(self, response):
        product_item = Product()
        product_item['name'] = self.product_name(response)
        product_item['retailer_sku'] = self.product_id(response)
        product_item['brand'] = " HELLYHANSEN"
        product_item['lang'] = self.product_lang(response)
        product_item['description'] = self.product_description(response)
        product_item['image_urls'] = self.image_links(response)
        product_item['care'] = self.product_care(response)
        product_item['category'] = self.product_categories(response)
        product_item['gender'] = self.product_gender(response)
        product_item['url'] = response.url
        product_item['skus'] = self.skus(response)
        
        return product_item

    def product_name(self, response):
        return response.css('.heading--page-title span.base::text').get()

    def product_id(self, response):
        return response.css('.sku .value::text').get()
    
    def product_lang(self, response):
        return response.css('html::attr(lang)').get()

    def product_categories(self, response):
        return response.css('.nosto_product .categories .category::text').getall()

    def product_description(self, response):
        description1 = response.css('.nosto_product .description::text').getall()
        description2 = response.css('.nosto_product .description p::text').getall()
        return list(map(str.strip, description1 + description2))

    def product_care(self, response):
        care1 = response.css(".nosto_product .features::text").getall()
        care2 = response.css(".nosto_product .features p::text").getall()
        return care1 or care2

    def product_gender(self, response):
        soup = ' '.join(self.product_categories(response)).lower()
        for gender in self.possible_genders:
            if gender.lower() in soup:
                return gender

    def image_links(self, response):
        return response.css('.nosto_sku .image_url::text').getall()

    def skus(self, response):
        raw_skus = response.css('.nosto_sku')
        skus = {}
        currency = response.css(".nosto_product .price_currency_code::text").get()
        for raw_sku in raw_skus:
            color = raw_sku.css(".color::text").get()
            size = raw_sku.css(".size::text").get()
            price = raw_sku.css(".price::text").get()
            list_prices = raw_sku.css(".list_price::text").getall()
            sku = {
                "size": size,
                "price": price,
                "currency": currency,
                "previous_prices": list_prices
            }
            if 'outofstock' in raw_sku.css(".availability::text").get().lower():
                sku['out_of_stock'] = True
            if color:
                sku['colour'] = color
                skus[f"{color}_{size}"] = sku
            else:
                skus[f"{size}"] = sku

        return skus
