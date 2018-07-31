import re
import json

import scrapy


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
        listing_css = '#main-nav a::attr(href)'

        for url in response.css(listing_css).extract():
            yield response.follow(url, self.parse_listing)

    def parse_listing(self, response):
        product_css = '.product-image::attr(href)'

        for url in response.css(product_css).extract():
            yield response.follow(url, self.parse_product)

    def parse_product(self, response):
        return {
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
        categories = response.css('.breadcrumbs a::text').extract()
        return categories[1:]

    @staticmethod
    def get_product_name(response):
        return response.css('.product-name h1::text').extract_first()

    @staticmethod
    def get_product_description(response):
        description = response.css('#description div div::text').extract_first()
        return [d.strip() for d in description.split('. ') if '%' not in d]

    @staticmethod
    def get_product_care(response):
        care = response.css('#description div div::text').extract_first()
        return [c.strip() for c in care.split('. ') if '%' in c]

    def get_product_images(self, response):
        retailer_sku = self.get_product_retailer_sku(response)
        product_gallery = response.css('.product-image-gallery img::attr(src)').extract()
        retailer_sku_lowercase = retailer_sku.lower()
        return [i.replace('600x', '1800x') for i in product_gallery
                if retailer_sku_lowercase in i.lower()]

    @staticmethod
    def get_product_retailer_sku(response):
        return response.url.split('-')[-1]

    @staticmethod
    def get_product_gender(response):
        gender_map = {'women_apparel_size_label': 'female', 'men_apparel_size_label': 'male'}
        size_label = response.xpath('//dt/label[contains(@id, "size")]/@id').extract_first()
        return gender_map.get(size_label)

    @staticmethod
    def get_product_currency(response):
        currency_xpath = '//script[contains(text(), "currency")]'
        return response.xpath(currency_xpath).re(r'currency: \'([A-Z]+)\'')[0]

    def get_product_skus(self, response):
        skus = []
        colors = response.css('#configurable_swatch_color li')
        sizes = response.css('.configurable-swatch-list.configurable-block-list.clearfix li')
        common_pricing = self.get_product_prices(response)
        raw_product = self.get_raw_product(response)
        currency = self.get_product_currency(response)

        for color_sel in colors:
            color_code, color_name = self.get_product_color(color_sel)
            for size_sel in sizes:
                sku = common_pricing.copy()
                size_code, size_name = self.get_product_size(size_sel)
                key = f"{color_code},{size_code}"
                raw_sku = raw_product.get(key)
                if not raw_sku:
                    continue

                sku['sku_id'] = raw_sku.get('product_id')
                sku['color'] = color_name
                sku['currency'] = currency
                sku['size'] = size_name
                sku['out_of_stock'] = not raw_sku.get('is_in_stock')

                skus.append(sku)
        return skus

    @staticmethod
    def get_product_size(response):
        size_code = response.css('li::attr(id)').re(r'\d+')[0]
        size_text = response.css('a::attr(name)').extract_first()
        return size_code, size_text

    @staticmethod
    def get_product_color(response):
        color_code = response.css('li::attr(id)').re(r'\d+')[0]
        color_text = response.css('a::attr(name)').extract_first()
        return color_code, color_text

    @staticmethod
    def get_raw_product(response):
        raw_product_xpath = '//*[@id="product-options-wrapper"]' \
                            '//script[contains(text(), "StockStatus")]/text()'
        script = response.xpath(raw_product_xpath).extract_first()
        stock_status_json = script.split('new StockStatus(')[1].split(')')[0]
        return json.loads(stock_status_json)

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d*.?\d*$', string)[0]
        return int(float(price.replace(',', '')) * 100)

    def get_product_prices(self, response):
        prices = response.css('.product-shop .price-info .price::text').extract()
        prices = [self.get_price_from_string(price.strip()) for price in prices]

        product_price = {}

        if len(prices) > 1:
            product_price['price'] = prices.pop(-1)
            product_price['previous_price'] = prices
        else:
            product_price['price'] = prices[0]

        return product_price
