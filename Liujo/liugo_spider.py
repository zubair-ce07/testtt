import re
import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'liujo-uk'
    market = 'UK'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb/']
    gender = 'women'


class LiujoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-main-info .price::text'
    regex_sku = re.compile('Product.Config\((.*)\)')

    def parse(self, response):

        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def create_sku(self, data, code, type, raw_skus):
        if code in data['attributes']:
            for element in data['attributes'][code]['options']:
                for product in element['products']:
                    raw_skus.setdefault(product, {})[type] = element['label']

    def create_raw_skus(self, data):
        raw_skus = {}

        self.create_sku(data, '92', 'color', raw_skus)
        self.create_sku(data, '179', 'size', raw_skus)

        return raw_skus

    def skus(self, response):
        common = self.product_pricing_common_new(response)
        if self.regex_sku.search(response.text):
            data = json.loads(self.regex_sku.search(response.text).group(1))
            raw_skus = self.create_raw_skus(data)

            for sku in raw_skus:
                raw_skus[sku].update(common)

        else:
            common['size'] = self.one_size
            return {
                self.one_size: common
            }

        return raw_skus

    def product_category(self, response):
        return [t for t, _ in response.meta['trail'] if t] if 'trail' in response.meta else ''

    def image_urls(self, response):
        return clean(response.css('.product-media-gallery img::attr(data-more-views)'))

    def product_id(self, response):
        return clean(response.css('.product-ids::text'))[0].replace('Item ', '')

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_description(self, response):
        return clean(response.css('.short-description-value ::text')) + [care for care in clean(response.css('.details-value ::text')) if not self.care_criteria_simplified(care)]

    def product_care(self, response):
        return [care for care in clean(response.css('.details-value ::text')) if self.care_criteria_simplified(care)]

    def product_brand(self, response):
        return 'Liujo'


class LiujoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LiujoParseSpider()

    listing_css = ['.second-level [target="_self"]', '[rel="next"]']

    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item')
    )
