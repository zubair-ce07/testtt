import re

import scrapy

from ..items import SnkrsItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://snkrs.com/en/']

    def parse(self, response):
        [(yield response.follow(url, callback=self.parse_listing_page))
        for url in response.css('.a-niveau1::attr(href)').getall()]

    def parse_listing_page(self, response):
        [(yield response.follow(url, callback=self.parse_product_page))
        for url in response.css('.product_img_link::attr(href)').getall()]

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
        items['skus'] = self.get_skus(items, response)

        yield items

    def get_skus(self, items, response):
        get_colour = re.sub(r'.*- ', '', items['name'])
        price = response.css('div.nosto_product .price::text').get()
        float_price = float(price)
        skus = {}

        for sizes in response.css('span.units_container .size_EU::text').getall():
            skus[get_colour + "_" + sizes] = {
                "colour": get_colour,
                "currency": response.css('.nosto_product .price_currency_code::text').get(),
                "price": float_price,
                "old_price": response.xpath('//span[@id="old_price_display"]/span/text()').get(),
                "size": sizes
            }
            skus.update(skus)

        return skus

    def get_retailer_sku(self, response):
        return response.css('.nosto_product .product_id::text').getall()[0]

    def get_brand(self, response):
        return response.css('.nosto_product .brand::text').get()

    def get_category(self, response):
        return response.css('div.nosto_category::text').get()

    def get_desciption(self, response):
        reference = '//p[@id="product_reference"]/label/text()'
        description = ' //div[@id="short_description_content"]/p/text()'
        return response.xpath(reference + ' | ' + description).getall()

    def get_gender(self, response):
        gender = response.css('.nosto_category::text').re_first(r'(Men|Women)')

        return "men" if gender == "Men" else "women" if gender == "Women" else "unisex-adults"

    def get_name(self, response):
        return response.css('.nosto_product .name::text').get()

    def get_image_urls(self, response):
        return response.css('.image_url::text, .alternate_image_url::text').getall()
