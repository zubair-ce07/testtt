import re
import json
from collections import namedtuple

import scrapy

Size = namedtuple('Size', ['code', 'text'])
Color = namedtuple('Color', ['code', 'text'])
SKUVariant = namedtuple('SKUVariant', ['color', 'size', 'prices'])


class APCUSSpider(scrapy.Spider):
    name = "apc_us"
    start_urls = [
        'https://www.apc-us.com'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'apc-us.com'
    ]

    def parse(self, response):
        listing_css = '#main-nav a'

        for url_selector in response.css(listing_css):
            url = self.extract_from_css('a::attr(href)', url_selector)
            yield response.follow(url, self.parse_listing)

    def parse_listing(self, response):
        product_css = 'a.product-image'

        for url_selector in response.css(product_css):
            url = self.extract_from_css('a::attr(href)', url_selector)
            yield response.follow(url, self.parse_product)

    def parse_product(self, response):
        yield {
            'retailer_sku': self.get_product_retailer_sku(response),
            'name': self.get_product_name(response),
            'category': self.get_product_categories(response),
            'description': self.get_product_description(response),
            'image_urls': self.get_product_images(response),
            'url': response.url,
            'gender': self.get_product_gender(response),
            'brand': 'A.P.C.',
            'care': self.get_product_care(response),
            'skus': self.get_product_skus(response)
        }

    @staticmethod
    def get_product_categories(response):
        categories = response.css('div.breadcrumbs a::text').extract()
        return categories[1:]

    @staticmethod
    def extract_from_css(query, response):
        result = response.css(query).extract()
        if len(result) == 1:
            return result[0]

        return result

    def get_product_name(self, response):
        return self.extract_from_css('div.product-name h1::text', response)

    @staticmethod
    def get_product_description(response):
        description = response.css('section#description div > div::text').extract_first()
        return [d.strip() for d in description.split('. ') if '%' not in d]

    @staticmethod
    def get_product_care(response):
        care = response.css('section#description div > div::text').extract_first()
        return [c.strip() for c in care.split('. ') if '%' in c]

    def get_product_images(self, response):
        retailer_sku = self.get_product_retailer_sku(response)
        product_gallery = self.extract_from_css('div.product-image-gallery img::attr(src)',
                                                response)
        return [i.replace('600x', '1800x') for i in product_gallery
                if retailer_sku.lower() in i.lower()]

    @staticmethod
    def get_product_retailer_sku(response):
        return response.url.split('-')[-1]

    @staticmethod
    def get_product_gender(response):
        gender_map = {'women_apparel_size_label': 'female', 'men_apparel_size_label': 'male'}
        size_label = response.xpath('//dt/label[contains(@id, "size")]/@id').extract_first()
        return gender_map.get(size_label)

    @staticmethod
    def generate_product_sku(sku_variant, raw_product):
        sku = {}
        key = f"{sku_variant.color.code},{sku_variant.size.code}"
        raw_sku = raw_product.get(key)
        if not raw_sku:
            return

        sku['sku_id'] = raw_sku.get('product_id')
        sku['color'] = sku_variant.color.text
        sku['currency'] = 'USD'
        sku['size'] = sku_variant.size.text
        sku['out_of_stock'] = not raw_sku.get('is_in_stock')

        if len(sku_variant.prices) > 1:
            sku['previous_price'] = sku_variant.prices[0]
            sku['price'] = sku_variant.prices[1]
        else:
            sku['price'] = sku_variant.prices[0]

        return sku

    def get_product_skus(self, response):
        skus = []
        colors = self.get_product_colors(response)
        sizes = self.get_product_sizes(response)
        prices = self.get_product_prices(response)
        raw_product = self.get_raw_product(response)

        for color in colors:
            for size in sizes:
                sku = self.generate_product_sku(SKUVariant(color, size, prices), raw_product)
                if sku:
                    skus.append(sku)

        return skus

    def get_product_sizes(self, response):
        sizes = []
        size_responses = response.css(
            'ul.configurable-swatch-list.configurable-block-list.clearfix li')

        for size_response in size_responses:
            size_code = self.extract_from_css('li::attr(id)', size_response)
            size_code = re.findall(r'\d+', size_code)[0]
            size_text = self.extract_from_css('a::attr(name)', size_response)
            sizes.append(Size(size_code, size_text))

        return sizes

    def get_product_colors(self, response):
        colors = []
        color_responses = response.css('#configurable_swatch_color li')

        for color_response in color_responses:
            color_code = self.extract_from_css('li::attr(id)', color_response)
            color_code = re.findall(r'\d+', color_code)[0]
            color_text = self.extract_from_css('a::attr(name)', color_response)
            colors.append(Color(color_code, color_text))

        return colors

    @staticmethod
    def get_raw_product(response):
        script_div = response.css('#product-options-wrapper')
        script = script_div.xpath('//script[contains(text(), "StockStatus")]/text()'
                                  ).extract_first()
        stock_status_json = script.split('new StockStatus(')[1].split(')')[0]
        return json.loads(stock_status_json)

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d*.?\d*$', string)[0]
        return int(float(price.replace(',', '')) * 100)

    def get_product_prices(self, response):
        prices = response.css('div.product-shop div.price-info span.price::text').extract()
        return [self.get_price_from_string(price.strip()) for price in prices]
