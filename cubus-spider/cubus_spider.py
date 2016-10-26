# -*- coding: utf-8 -*-
import re
import json
import math
from urlparse import parse_qsl, urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import FormRequest

from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser


class Mixin(object):
    retailer = 'cubus'
    allowed_domains = ['cubus.com']


class MixinSV(Mixin):
    retailer = Mixin.retailer + '-sv'
    market = 'SV'
    lang = 'sv'
    url_prefix = 'https://cubus.com/sv/'
    start_urls = ['https://cubus.com/sv']
    product_post_url = 'https://cubus.com/sv/api/product/post'
    gender_map = (
        ('herr', 'men'),
        ('dam', 'women'),
        ('pojke', 'boys'),
        ('flicka', 'girls'),
        ('baby', 'unisex-kids'),
    )


class MixinNO(Mixin):
    retailer = Mixin.retailer + '-no'
    market = 'NO'
    lang = 'no'
    url_prefix = 'https://cubus.com/no/'
    start_urls = ['https://cubus.com/no']
    product_post_url = 'https://cubus.com/no/api/product/post'
    gender_map = (
        ('dame', 'women'),
        ('herre', 'men'),
        ('gutt', 'boys'),
        ('jente', 'girls'),
        ('baby', 'unisex-kids'),
    )

class CubusParseSpider(BaseParseSpider):

    def parse(self, raw_product, meta=None):
        product_id = clean(raw_product['Code'])
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_minimal(garment, raw_product, meta=meta)
        garment['name'] = clean(raw_product['Name'])
        garment['brand'] = clean(raw_product['ProductBrand'])
        garment['care'] = self.product_care(raw_product)
        garment['image_urls'] = self.product_images(raw_product)
        garment['skus'] = self.skus(raw_product)
        garment['gender'] = self.product_gender(garment['trail'])
        garment['category'] = self.product_category(garment['trail'])

        return garment

    def boilerplate_minimal(self, garment, raw_product, meta=None):
        garment['trail'] = meta['trail']
        garment['url'] = urljoin(self.url_prefix, raw_product['Url'])
        garment['date'] = self.utc_now()
        garment['uuid'] = None
        garment['market'] = self.market
        garment['retailer'] = self.retailer
        garment['product_hash'] = self.generate_product_hash_for_garment(garment)
        garment['crawl_id'] = self.crawl_id

    def product_category(self, trail):
        return [clean(category[0]) for category in filter(lambda t: t[0] != '', trail)]

    def product_gender(self, trail):
        soup = ''.join([t[1] for t in trail]).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-kids'

    def product_images(self, raw_product):
        return [urljoin('https://cubus.com', url['ZoomImage']) for url in raw_product['MediaCollection']]

    def product_care(self, raw_product):
        care = []
        for raw_care in raw_product['ProductCare']:
            care += [clean(raw_care + ':' + raw_product['ProductCare'][raw_care])]
        if 'Composition' in raw_product:
            care += [clean(raw_product['Composition'])]

        return care

    def skus(self, raw_product):
        skus = {}

        for raw_sku in raw_product['Skus']:
            sku = {}
            sku['colour'] = clean(raw_product['VariantColor']['Label'])
            sku['size'] = clean(raw_sku['Size'])
            sku['currency'] = raw_product['OfferedPrice']['Currency']
            sku['price'] = CurrencyParser.lowest_price(str(raw_product['OfferedPrice']['Price']))
            prev_price = CurrencyParser.lowest_price(str(raw_product['ListPrice']['Price']))

            if sku['price'] != prev_price:
                sku['previous_prices'] = [prev_price]

            if raw_sku['Quantity'] == 0:
                sku['out_of_stock'] = True

            skus[clean(raw_sku['Id'])] = sku

        return skus


class CubusCrawlSpider(BaseCrawlSpider):

    listings_css = [
        '.site-sub-navigation-secondary-list a'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_paging'),
    )
    products_per_page = 20

    def parse_paging(self, response):
        script_elements = response.css('script ::text').extract()
        for script in script_elements:
            catalog = re.findall('currentCatalogNode="(.+?)"', script)
            if catalog:
                yield self.xhr_post_request(catalog[0], 0, meta={'trail': self.add_trail(response)})

    def xhr_post_request(self, catalog, page, meta=None):
        form_data = {
            'Language': self.lang,
            'MarketId': '8WS',
            'CatalogNode': catalog,
            'Page': str(page),
            'FetchAllPages': 'false',
            'PriceFrom': '0',
            'PriceTo': '0',
            'Sorting': 'StyleInStockFrom',
            'ItemsPerPage': str(self.products_per_page),
            'ProductSearchPageId': '0'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
        }
        return FormRequest(self.product_post_url, formdata=form_data, headers=headers,
                           callback=self.parse_products, method='POST', meta=meta)

    def parse_products(self, response):
        raw_products = json.loads(response.text)

        return [self.parse_spider.parse(p, meta=response.meta) for p in raw_products['Products']] + \
               self.paging_requests(response.request.body, raw_products, meta=response.meta)

    def paging_requests(self, request_body, raw_products, meta=None):
        total_pages = math.ceil(raw_products['TotalCount'] / self.products_per_page) + 1
        raw_formdata = parse_qsl(request_body)
        formdata = dict(raw_formdata)

        return [self.xhr_post_request(formdata['CatalogNode'], i, meta=meta) for i in range(1, total_pages)]


class CubusParseSpiderSV(CubusParseSpider, MixinSV):
    name = MixinSV.retailer + '-parse'


class CubusCrawlSpiderSV(CubusCrawlSpider, MixinSV):
    name = MixinSV.retailer + '-crawl'
    parse_spider = CubusParseSpiderSV()


class CubusParseSpiderNO(CubusParseSpider, MixinNO):
    name = MixinNO.retailer + '-parse'


class CubusCrawlSpiderNO(CubusCrawlSpider, MixinNO):
    name = MixinNO.retailer + '-crawl'
    parse_spider = CubusParseSpiderNO()
