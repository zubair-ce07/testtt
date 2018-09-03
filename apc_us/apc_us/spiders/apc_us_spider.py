import json
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


class Sku(scrapy.Item):
    sku_id = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    out_of_stock = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    previous_price = scrapy.Field()


class Product(scrapy.Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    skus = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    gender_map = {'women_apparel_size_label': 'female', 'men_apparel_size_label': 'male'}

    @staticmethod
    def fetch_category(categories):
        return categories[1:]

    def fetch_gender(self, size_label):
        return self.gender_map.get(size_label[0])

    @staticmethod
    def fetch_description(description):
        description = description[0]
        return [d.strip() for d in description.split('. ') if '%' not in d]
    
    @staticmethod
    def fetch_care(care):
        care = care[0]
        return [d.strip() for d in care.split('. ') if '%' in d]

    @staticmethod
    def fetch_images(product_gallery, loader_context):
        retailer_sku = loader_context.get('response').url.split('-')[-1]
        retailer_sku_lowercase = retailer_sku.lower()
        return [i.replace('600x', '1800x') for i in product_gallery
                if retailer_sku_lowercase in i.lower()]

    category_in = fetch_category
    gender_in = fetch_gender
    description_in = fetch_description
    care_in = fetch_care
    image_urls_in = fetch_images

    category_out = Identity()
    image_urls_out = Identity()
    description_out = Identity()
    care_out = Identity()
    skus_out = Identity()


class SkuLoader(ItemLoader):
    default_output_processor = TakeFirst()


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
        product_loader = ProductLoader(item=Product(), response=response)

        product_loader.add_css('name', '.product-name h1::text')
        product_loader.add_css('category', '.breadcrumbs a::text')
        product_loader.add_css('description', '#description div div::text')
        product_loader.add_css('image_urls', '.product-image-gallery img::attr(src)')
        product_loader.add_css('care', '#description div div::text')
        product_loader.add_value('brand', 'A.P.C.')
        product_loader.add_value('retailer_sku', response.url.split('-')[-1])
        product_loader.add_value('url', response.url)
        product_loader.add_value('skus', self.get_product_skus(response))
        product_loader.add_xpath('gender', '//dt/label[contains(@id, "size")]/@id')

        return product_loader.load_item()

    @staticmethod
    def get_product_currency(response):
        currency_xpath = '//script[contains(text(), "currency")]'
        return response.xpath(currency_xpath).re(r'currency: \'([A-Z]+)\'')[0]

    def get_product_skus(self, response):
        colors = response.css('#configurable_swatch_color li')
        sizes = response.css('.configurable-swatch-list.configurable-block-list.clearfix li')
        common_pricing = self.get_product_prices(response)
        raw_product = self.get_raw_product(response)
        currency = self.get_product_currency(response)

        for color_sel in colors:
            color_code, color_name = self.get_product_color(color_sel)
            for size_sel in sizes:
                sku_loader = SkuLoader(item=Sku(), response=response)
                for price in common_pricing.keys():
                    sku_loader.add_value(price, common_pricing[price])

                size_code, size_name = self.get_product_size(size_sel)
                key = f"{color_code},{size_code}"
                raw_sku = raw_product.get(key)
                if not raw_sku:
                    continue

                sku_loader.add_value('sku_id', raw_sku.get('product_id'))
                sku_loader.add_value('color', color_name)
                sku_loader.add_value('currency', currency)
                sku_loader.add_value('size', size_name)
                sku_loader.add_value('out_of_stock', not raw_sku.get('is_in_stock'))

                yield sku_loader.load_item()

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
