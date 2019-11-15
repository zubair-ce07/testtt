import re

import scrapy

from ..items import SnkrsItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://snkrs.com/en/']

    def parse(self, response):
        urls = response.css('a.a-niveau1::attr(href)').getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        urls = response.css('.product_img_link::attr(href)').getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        items = SnkrsItem()

        items['retailer_sku'] = self.get_retailer_sku(response)
        items['brand'] = self.get_brand(response)
        items['category'] = self.get_category(response)
        items['description'] = self.get_desciption(response)
        items['gender'] = self.get_gender(response)
        items['url'] = response.url
        items['name'] = self.get_name(response)
        items['image_urls'] = self.get_image_urls(response)
        shoes_name = items['name']
        get_colour = re.sub(r'.*- ', '', shoes_name)

        for sizes in response.css(
                'span.units_container .size_EU::text').getall():
            items['skus'] = {
                get_colour +
                "_" +
                sizes: {
                    "colour": get_colour,
                    "currency": response.css('div.nosto_product span.price_currency_code::text').get(),
                    "price": response.css('div.nosto_product span.price::text').get(),
                    "old_price": response.xpath('//span[@id="old_price_display"]/span/text()').get(),
                    "size": sizes},
            }
            yield items['skus']

        yield items

    def get_retailer_sku(self, response):
        return response.css('div.nosto_product span.product_id::text').get()

    def get_brand(self, response):
        return response.css('div.nosto_product span.brand::text').get()

    def get_category(self, response):
        return response.css('div.nosto_category::text').get()

    def get_desciption(self, response):
        return response.css('div.rte p::text').getall()

    def get_gender(self, response):
        gender = response.css('div.nosto_category::text').re_first(
            r'(Men|Women|Skate|Lifestyle)')

        if gender == 'Men':
            gender = 'men'
            return gender

        elif gender == 'Women':
            gender = 'women'
            return gender

        else:
            gender = 'unisex-adults'
            return gender

    def get_name(self, response):
        return response.css('div.nosto_product span.name::text').get()

    def get_image_urls(self, response):
        return response.css('div.nosto_product .image_url::text').getall(), response.css(
            'div.nosto_product' + ' .alternate_image_url::text').getall()
