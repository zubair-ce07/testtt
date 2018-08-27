import json

from scrapy import Spider, Request

from lanebryant.items import LanebryantItem


class ProductParser(Spider):
    name = 'lanebryant-parser'
    brand = 'LB'
    gender = 'female'

    def parse(self, response):
        item = LanebryantItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trails(response)
        item['gender'] = self.gender
        # item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        # item['image_urls'] = self.extract_image_urls(response)
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        item['skus'] = self.extract_skus(response)
        return item

    def extract_retailer_sku(self, response):
        return response.css('::attr(data-bv-product-id)').extract_first()

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css('.mar-product-title::text').extract_first()

    def extract_product_description(self, response):
        description = response.css('div#tab1 p::text').extract()
        description += response.css('div#tab1 ul:nth-child(2) ::text').extract()
        return description

    def extract_product_care(self, response):
        return response.css('div#tab1 ul:nth-child(3) ::text').extract()

    def extract_raw_product(self, response):
        return json.loads(response.css('#pdpInitialData::text').extract_first())

    def extract_price_specification(self, response):
        price_specification_css = "[type='application/ld+json']::text"
        return json.loads(response.css(price_specification_css).extract_first())

    def extract_price(self, response):
        raw_price = self.extract_price_specification(response)
        return raw_price['offers']['priceSpecification']['price']

    def extract_currency(self, response):
        raw_currency = self.extract_price_specification(response)
        return raw_currency['offers']['priceSpecification']['priceCurrency']

    def extract_raw_skus(self, response):
        raw_skus = self.extract_raw_product(response)
        return raw_skus['pdpDetail']['product'][0]['skus']

    def extract_color(self, raw_product, color_id):
        raw_colors = raw_product['pdpDetail']['product'][0]['all_available_colors'][0]['values']
        for color in raw_colors:
            if color_id == color['id']:
                return color['name']

    def extract_skus(self, response):
        raw_product = self.extract_raw_product(response)
        raw_skus = self.extract_raw_skus(response)
        currency = self.extract_currency(response)
        for sku in raw_skus:
            sku['color'] = self.extract_color(raw_product, sku['color'])
            sku['currency'] = currency
        return raw_skus
