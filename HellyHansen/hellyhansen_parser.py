# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import Product

class HellyhansenParser(Spider):
    name = 'hellyhansenparser'
    allowed_domains = ['hellyhansen.com']
    start_urls = ['http://hellyhansen.com/en_gb/']
    possible_genders = ['Men', 'Women', 'Kids']

    def parse_product(self, response):
        product_item = Product()
        product_item['name'] = response.css('.heading--page-title span.base::text').get()
        product_item['retailer_sku'] = response.css('.sku .value::text').get()
        product_item['brand'] = " HELLYHANSEN"
        product_item['lang'] = response.css('html::attr(lang)').get()
        product_item['description'] = self.parse_description(response).strip()
        product_item['image_urls'] = self.parse_image_links(response)
        product_item['category'] = self.parse_categories(response)
        product_item['gender'] = self.parse_gender(response)
        product_item['url'] = response.request.url
        product_item['skus'] = self.parse_skus(response)
        product_item['care'] = self.parse_care(response)
        
        return product_item

    def parse_categories(self, response):
        return response.css('.nosto_product .categories .category::text').getall()

    def parse_description(self, response):
        description1 = response.css('.nosto_product .description::text').get()
        description2 = '\n'.join(response.css('.nosto_product .description p::text').getall())
        if description1:
            description1 = description1.strip()
        return description1 or description2

    def parse_care(self, response):
        care1 = response.css(".nosto_product .features::text").getall()
        care2 = response.css(".nosto_product .features p::text").getall()
        return care1 or care2

    def parse_gender(self, response):
        soup = ' '.join(self.parse_categories(response)).lower()
        for gender in self.possible_genders:
            if gender.lower() in soup:
                return gender

    def parse_image_links(self, response):
        image_urls = response.css('.nosto_sku .image_url::text').getall()
        return list(dict.fromkeys(image_urls))

    def parse_skus(self, response):
        raw_skus = response.css('.nosto_sku')
        skus = {}
        currency = response.css(".nosto_product .price_currency_code::text").get()
        for raw_sku in raw_skus:
            color = raw_sku.css(".color::text").get()
            size = raw_sku.css(".size::text").get()
            price = raw_sku.css(".price::text").get()
            list_prices = raw_sku.css(".list_price::text").getall()
            sku = {
                "colour": color,
                "size": size,
                "price": price,
                "currency": currency,
                "previous_prices": list_prices
            }
            if 'outofstock' in raw_sku.css(".availability::text").get().lower():
                sku['out_of_stock'] = True
            skus[f"{color}_{size}"] = sku

        return skus
