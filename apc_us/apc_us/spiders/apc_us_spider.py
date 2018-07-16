import re
import json
from collections import namedtuple

import scrapy

Size = namedtuple('Size', ['code', 'text'])
Color = namedtuple('Color', ['code', 'text'])


class APCUSSpider(scrapy.Spider):
    name = "apc_us"
    start_urls = [
        'https://www.apc-us.com'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        for link in response.css('a'):
            url = self.extract_from_css('a::attr(href)', link)

            if 'apc-us.com' in url:
                if self.is_product_url(link):
                    yield response.follow(url, self.parse_product)
                else:
                    yield response.follow(url, self.parse)

    def is_product_url(self, response):
        if self.extract_from_css('a.product-image::attr(href)', response):
            return True

        return False

    def parse_product(self, response):
        retailer_sku = self.get_product_retailer_sku(response)
        gender = self.get_product_gender(response)
        prices = self.get_product_prices(response)

        yield {
            'retailer_sku': retailer_sku,
            'name': self.get_product_name(response),
            'category': self.get_product_categories(response),
            'description': self.get_product_description(response),
            'image_urls': self.get_product_images(response, retailer_sku),
            'url': response.url,
            'gender': gender,
            'brand': 'A.P.C.',
            'care': self.get_product_care(response),
            'skus': self.get_product_skus(response, gender, prices)
        }

    @staticmethod
    def get_product_categories(response):
        categories = response.css('div.breadcrumbs a::text').extract()
        categories.remove('Home')
        return categories

    @staticmethod
    def extract_from_css(query, response):
        result = response.css(query).extract()
        if len(result) == 1:
            return result[0]

        return result

    @staticmethod
    def search_in_list(query, string_list, search_flags=0):
        r = re.compile(query, flags=search_flags)
        return list(filter(r.search, string_list))

    @staticmethod
    def inverse_search_in_list(query, string_list, search_flags=0):
        r = re.compile(query, flags=search_flags)
        return list(filter(lambda v: not r.search(v), string_list))

    def get_product_name(self, response):
        return self.extract_from_css('div.product-name h1::text', response)

    def get_product_description(self, response):
        description = response.css('section#description div > div::text').extract_first()
        string_to_sentence = re.compile(r'\. ')
        description = [d.strip() for d in string_to_sentence.split(description)]
        return self.inverse_search_in_list(r'%', description)

    def get_product_care(self, response):
        care = response.css('section#description div > div::text').extract_first()
        string_to_sentence = re.compile(r'\. ')
        care = [c.strip() for c in string_to_sentence.split(care)]
        return self.search_in_list(r'%', care)

    def get_product_images(self, response, retailer_sku):
        product_gallery = self.extract_from_css('div.product-image-gallery img::attr(src)',
                                                response)
        small_images = self.search_in_list(
            retailer_sku, product_gallery, search_flags=re.IGNORECASE)
        return [re.sub(r'600x', r'1800x', i) for i in small_images]

    @staticmethod
    def get_product_retailer_sku(response):
        return response.url.split('-')[-1]

    def get_product_gender(self, response):
        if self.extract_from_css('#women_apparel_size_label', response):
            return 'female'

        if self.extract_from_css('#men_apparel_size_label', response):
            return 'male'

        if self.extract_from_css('#size_label', response):
            return 'none'

        return 'undefined'

    @staticmethod
    def generate_product_sku(color, size, product_json, prices):
        sku = {}
        key = f"{color.code},{size.code}"
        sku_json = product_json.get(key)
        if not sku_json:
            return

        sku['sku_id'] = sku_json['product_id']
        sku['color'] = color.text
        sku['currency'] = 'USD'
        sku['size'] = size.text
        sku['out_of_stock'] = not sku_json['is_in_stock']

        if type(prices) is list:
            sku['previous_price'] = prices[0]
            sku['price'] = prices[1]
        else:
            sku['price'] = prices

        return sku

    def get_product_skus(self, response, gender, prices):
        skus = []
        colors = self.get_product_colors(response)
        sizes = self.get_product_sizes(response, gender)
        product_json = self.get_product_json(response)

        for color in colors:
            for size in sizes:
                sku = self.generate_product_sku(color, size, product_json, prices)
                if sku:
                    skus.append(sku)

        return skus

    def get_product_sizes(self, response, gender):
        sizes = []

        if gender == 'male':
            size_responses = response.css('#configurable_swatch_men_apparel_size li')
        elif gender == 'female':
            size_responses = response.css('#configurable_swatch_women_apparel_size li')
        elif gender == 'none':
            size_responses = response.css('#configurable_swatch_size li')
        else:
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
    def get_product_json(response):
        script = response.css('#product-options-wrapper > script:nth-child(1)').extract_first()
        stock_status_json = script.split('new StockStatus(')[1].split(')')[0]
        return json.loads(stock_status_json)

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d*.?\d*$', string)[0]
        return int(float(price.replace(',', '')) * 100)

    def get_product_prices(self, response):
        prices = self.extract_from_css('div.product-shop div.price-info span.price::text', response)
        if type(prices) is list:
            return [self.get_price_from_string(price.strip()) for price in prices]

        return self.get_price_from_string(prices.strip())
