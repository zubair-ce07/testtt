import re
import json
from collections import namedtuple

import scrapy

Size = namedtuple('Size', ['code', 'text'])
Color = namedtuple('Color', ['code', 'text'])
SKUVariant = namedtuple('SKUVariant', ['color', 'size', 'prices'])


class TausendkindSpider(scrapy.Spider):
    name = "tausendkind"
    start_urls = [
        'https://www.tausendkind.de/zoolaboo-t-shirt-big-shark-in-dunkelblau-91811121000'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'tausendkind.de'
    ]

    def parse(self, response):
        # ax = scrapy.Request(
        #     'https://www.tausendkind.de/zoolaboo-t-shirt-hai-gestreift-in-blau-weiss-89772001000',
        #     self.parse_product)
        ax = scrapy.Request(
            'https://www.tausendkind.de/zoolaboo-t-shirt-big-shark-in-dunkelblau-91811121000',
            self.parse_product)
        # ax = scrapy.Request(
        #     'https://www.tausendkind.de/zoolaboo-t-shirt-big-shark-in-dunkelblau-91811121000',
        #     self.parse_product_variant)
        yield ax

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)

        sku = {
            'retailer_sku': self.get_product_retailer_sku(raw_product),
            'name': self.get_product_name(raw_product),
            'brand': self.get_product_brand(raw_product),
            'gender': self.get_product_gender(raw_product),
            'category': self.get_product_categories(response),
            'url': response.url,
            'description': self.get_product_description(response),
            'care': self.get_product_care(response),
            'alt': self.get_color_urls(response)
        }

        if sku['alt']:
            request = scrapy.Request(sku['alt'].pop(), self.parse_product_variant)
            request.meta['sku'] = sku
            yield request

    def get_product_variants(self, response):
        color_url = self.get_color_urls(response)

        for alternative in color_url:
            yield scrapy.Request(alternative, self.parse_product_variant)

    def parse_product_variant(self, response):
        yield response.meta['sku']
        # product_variant = {'skus': []}
        # sizes_column = response.css('div.select__menu.select__menu--pdp li.select__option')
        # raw_images = self.get_raw_product_images(response)
        # color = response.css(
        #     'img.pdp-other-color--active::attr(alt)').extract_first().split(' in ')[-1]
        #
        # for row in sizes_column:
        #     sku = {
        #         'sku_id': row.css('li::attr(data-value)').extract_first(),
        #         'size': row.css('div.l-space::text').extract_first(),
        #         'is_in_stock': not row.xpath('.//div[contains(text(), "Ausverkauft")]').extract(),
        #         'currency': 'EUR',
        #         'color': color
        #     }
        #
        #     special_price = self.get_price_from_string(
        #         row.css('li::attr(data-specialprice)').extract_first())
        #     price = self.get_price_from_string(row.css('li::attr(data-price)').extract_first())
        #
        #     if special_price:
        #         sku['price'] = special_price
        #         sku['previous_price'] = price
        #     else:
        #         sku['price'] = price
        #
        #     product_variant['skus'].append(sku)
        #
        # product_variant['images'] = raw_images['images']['list']
        # yield product_variant

    @staticmethod
    def get_product_categories(response):
        categories = response.css('li.breadcrumb__li a::text').extract()
        return {c.strip() for c in categories[1:] if c.strip()}

    @staticmethod
    def get_color_urls(response):
        return response.css('div.alternatives-list-item a::attr(href)').extract()

    @staticmethod
    def get_product_retailer_sku(raw_product):
        return raw_product['product']['master_sku']

    @staticmethod
    def get_product_gender(raw_product):
        gender_map = {'junge': 'boy', 'maedchen': 'girl'}
        return gender_map.get(raw_product['product']['filter_gender'])

    @staticmethod
    def get_product_brand(raw_product):
        return raw_product['product']['manufacturer_name']

    @staticmethod
    def get_product_name(raw_product):
        return raw_product['product']['name']

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d+', string)[0]
        return int(float(price.replace(',', '.')) * 100)

    @staticmethod
    def get_product_description(response):
        description = response.css(
            'div.pdp-description-container--description p::text').extract_first()
        return [d.strip() for d in re.split(r'[.,]', description) if d.strip()]

    @staticmethod
    def get_raw_product_images(response):
        script = response.xpath('//script[contains(text(), "tkd_product")]').extract_first()
        raw_images = script.split('tkd_product\', ')[1].split(');')[0]
        return json.loads(raw_images)

    @staticmethod
    def get_product_care(response):
        care = response.css('div.pdp-description-container--fabric_and_care li::text').extract()
        return [c for c in care[:-1] if 'Herstellerartikelnummer' not in c]

    @staticmethod
    def get_raw_product(response):
        script = response.xpath('//script[contains(text(), "master_sku")]').extract_first()
        raw_product = script.split('= [')[1].split('];')[0]
        return json.loads(raw_product)
