import json
from urllib.parse import urljoin

from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'nobis-us'
    market = 'US'
    product_listings_url = 'https://nobis-us.myshopify.com/api/apps/6/product_listings'
    product_listings_authorization = 'Basic ZTMyNjI1ZDJjZjAwNjUxMzNiYzI2MjUyNWM0YzMzOTY='
    allowed_domains = ['us.nobis.com', 'nobis-us.myshopify.com']
    start_urls = ['https://us.nobis.com/']
    gender_map = [
        ('woman', 'women'),
        ('women', 'women'),
        ('man', 'men'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-kids'),
    ]


class NobisParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_product = json.loads(response.text)
        garment = self.new_unique_garment(raw_product['id'])

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['brand'] = "Nobis"
        garment['name'] = raw_product['title']
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = raw_product['tags']
        garment['image_urls'] = raw_product['images']
        garment['skus'] = self.skus(raw_product)
        garment['gender'] = self.product_gender(garment)
        garment['url'] = self.product_url(response, raw_product)

        yield garment

    def product_url(self, response, raw_product):
        return response.urljoin(raw_product['url'])

    def product_description(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if not self.care_criteria_simplified(rd)]

    def product_care(self, raw_product):
        return [rd for rd in self.raw_description(raw_product) if self.care_criteria_simplified(rd)]

    def raw_description(self, raw_product):
        raw_description = raw_product.get('description', '')
        description_sel = Selector(text=raw_description)
        return clean(description_sel.css('::text'))

    def skus(self, raw_product):
        skus = {}
        common = {'currency': 'USD'}

        for variant in raw_product['variants']:
            skus[variant['id']] = sku = common.copy()

            fabric = variant['option3']
            size = variant['option1']
            sku['size'] = '{size}/{fabric}'.format(size=size, fabric=fabric) if fabric else size

            sku['colour'] = variant['option2']
            sku['price'] = variant['price']

            if variant['compare_at_price']:
                sku['previous_prices'] = [variant['compare_at_price']]

            if not variant['available']:
                sku['out_of_stock'] = True

        return skus

    def product_gender(self, garment):
        soup = ' '.join(garment['category']).lower()

        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'


class NobisCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = NobisParseSpider()

    listing_css = [
        'li[collection-item]'
    ]
    rules = [
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_categories')
    ]

    def parse_categories(self, response):
        product_listings_url = add_or_replace_parameter(self.product_listings_url,
                                                        "collection_id", self.get_collection_id(response))

        return Request(url=product_listings_url,
                       meta={'product_url': self.get_product_url(response)},
                       headers={'authorization': self.product_listings_authorization},
                       callback=self.parse_product_listings)

    def parse_product_listings(self, response):
        raw_product_listings = json.loads(response.text)['product_listings']
        for product in raw_product_listings:
            product_url = urljoin(response.meta['product_url'], "{}.js".format(product['handle']))
            yield Request(url=product_url, callback=self.parse_spider.parse)

    @staticmethod
    def get_collection_id(response):
        xpath = '//script[contains(.,"resourceId")]'
        return response.xpath(xpath).re(r'"resourceId":(\d+)')[0]

    @staticmethod
    def get_product_url(response):
        product_url = response.css('a[thumb-link]::attr(href)').extract_first()
        return response.urljoin(product_url)
