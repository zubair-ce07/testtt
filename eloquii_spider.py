import json

import re
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'eloquii'
    market = 'US'

    start_urls = ['https://www.eloquii.com/']
    allowed_domains = ['eloquii.com']
    api_url = 'https://www.eloquii.com/on/demandware.store/Sites-eloquii-Site/default/Product-GetVariants?'

    lang = 'en'
    currency = 'USD'
    gender = 'Women'


class EloquiiParser(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = ".description.pt-3 li:first-child ::text"
    care_css = '.description.pt-3 li:not(:first-child) ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.request_variants(product_id)}
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_id(response):
        return clean(response.css('.yotpo.yotpo-pictures-widget::attr(data-product-id)'))[0]

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb.bg-white .text-12::text'))

    @staticmethod
    def product_name(response):
        return clean(response.xpath('//meta[@name="keywords"]/@content'))[0]

    def image_urls(self, response):
        image_urls = []
        images = clean(response.xpath('//script[contains(text(),"app.execUjs")]/text()'))[0]
        images = re.findall('"Color", ("vals".*), {"id" : "size"', images)[0]
        images = json.loads("{" + images)
        for val in images.get('vals'):
            for images in val.get('images').get('large'):
                image_urls.append(response.urljoin(images.get('url')))
        return image_urls

    def request_variants(self, product_id):
        url = add_or_replace_parameter(self.api_url, 'pid', product_id)
        url = add_or_replace_parameter(url, 'format', 'ajax')
        return [Request(url, self.parse_variants)]

    def parse_variants(self, response):
        garment = response.meta['garment']
        variants = json.loads(response.text)
        for variant in variants.get('variations').get('variants'):
            if type(variant) is not dict:
                for fit in variant:
                    garment['skus'].update(self.skus(fit))
            else:
                garment['skus'].update(self.skus(variant))
        return self.next_request_or_garment(garment)

    def skus(self, variant):
        sku = {}
        sku['colour'] = variant.get('attributes').get('colorCode')
        sku['size'] = self.one_size if variant.get('size') == 'NS' else variant.get('size')
        sku['length'] = variant.get('sizeType')
        sku['price'] = variant.get('pricing').get('sale')
        sku['previous_prices'] = variant.get('pricing').get('standard')
        sku['currency'] = self.currency
        sku['out_of_stock'] = not variant.get('inStock')
        sku_id = f"{sku['colour']}_{sku['size']}"
        return {sku_id: sku}


class EloquiiCrawler(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = EloquiiParser()
    listing_css = [
        '.d-flex.justify-content-center li a',
        '.justify-content-center.mt-5 div:nth-child(3) a'
    ]
    product_css = '.product-images a:first-child'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)
             ),
        Rule(
            LinkExtractor(restrict_css=product_css), callback='parse_item'
        )
    )
