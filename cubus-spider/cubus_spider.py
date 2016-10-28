# -*- coding: utf-8 -*-
import re
import json
from urlparse import parse_qsl, urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import FormRequest

from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser


class Mixin(object):
    retailer = 'cubus'
    allowed_domains = ['cubus.com']
    global_resource_prefix = 'https://cubus.com'


class MixinSV(Mixin):
    retailer = Mixin.retailer + '-sv'
    market = 'SE'
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

    def parse(self, raw_garment, trail):

        product_id = clean(raw_garment['Style'])
        garment = self.new_garment(product_id)

        self.boilerplate_minimal(garment, raw_garment)
        garment['name'] = clean(raw_garment['Name'])
        garment['brand'] = clean(raw_garment['ProductBrand'])
        garment['care'] = self.product_care(raw_garment)
        garment['description'] = self.product_description(raw_garment)
        garment['image_urls'] = self.product_images(raw_garment)
        garment['skus'] = self.skus(raw_garment)
        garment['trail'] = trail
        garment['gender'] = self.product_gender(garment['trail'])
        garment['category'] = self.product_category(garment['trail'])

        return garment

    def boilerplate_minimal(self, garment, raw_product):

        garment['url'] = urljoin(self.url_prefix, raw_product['Url'])
        garment['url_original'] = garment['url']
        garment['date'] = self.utc_now()
        garment['uuid'] = None
        garment['market'] = self.market
        garment['retailer'] = self.retailer
        garment['product_hash'] = self.generate_product_hash_for_garment(garment)
        garment['crawl_id'] = self.crawl_id

    def product_category(self, trail):
        return clean([category[0] for category in trail if category[0]])

    def product_gender(self, trail):
        soup = ''.join([t[1] for t in trail]).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def product_images(self, raw_product):
        return [urljoin(self.global_resource_prefix, url['ZoomImage']) for url in raw_product['MediaCollection']]

    def product_description(self, raw_product):
        if 'ShortDescription' in raw_product:
            return [x for x in raw_product['ShortDescription'] if not self.care_criteria_simplified(x)]

        return []

    def product_care(self, raw_product):
        care = []

        if 'ShortDescription' in raw_product:
            care = [x for x in raw_product['ShortDescription'] if self.care_criteria_simplified(x)]

        for raw_care in raw_product['ProductCare']:
            care += [clean(raw_care + ':' + raw_product['ProductCare'][raw_care])]

        if 'Composition' in raw_product:
            care += [clean(raw_product['Composition'])]

        return care

    def skus(self, raw_garment):
        skus = {}

        for raw_sku in raw_garment['Skus']:
            sku = {}
            sku['colour'] = clean(raw_garment['VariantColor']['Label'])
            sku['size'] = clean(raw_sku['Size'])
            sku['currency'] = CurrencyParser.currency(raw_garment['OfferedPrice']['Currency'])
            sku['price'] = CurrencyParser.lowest_price(str(raw_garment['OfferedPrice']['Price']))
            previous_price = CurrencyParser.lowest_price(str(raw_garment['ListPrice']['Price']))

            if sku['price'] != previous_price:
                sku['previous_prices'] = [previous_price]

            if raw_sku['Quantity'] < 1:
                sku['out_of_stock'] = True

            skus[clean(raw_sku['Id'])] = sku

        return skus


class CubusCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.site-sub-navigation-secondary-list a'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),
    )

    def parse_category(self, response):
        script_elements = response.css('script ::text').extract()
        for script in script_elements:
            catalog = re.findall('currentCatalogNode="(.+?)"', script)
            if catalog:
                yield self.xhr_post_request(catalog[0], 0, callback=self.parse_paging,
                                            meta={'trail': self.add_trail(response)})

    def parse_paging(self, response):
        raw_products = json.loads(response.text)
        if raw_products['HaveMoreItems']:
            raw_formdata = parse_qsl(response.request.body)
            formdata = dict(raw_formdata)
            next_page = int(formdata['Page']) + 1
            yield self.xhr_post_request(formdata['CatalogNode'], next_page, meta=response.meta,
                                        callback=self.parse_paging)

        for raw_product in raw_products['Products']:
            yield self.parse_spider.parse(raw_product, response.meta['trail'])

    def xhr_post_request(self, catalog, page, meta=None, callback=None):

        form_data = {
            'Language': self.lang,
            'MarketId': '8WS',
            'CatalogNode': catalog,
            'Page': str(page),
            'FetchAllPages': 'false',
            'PriceFrom': '0',
            'PriceTo': '0',
            'Sorting': 'StyleInStockFrom',
            'ItemsPerPage': '0',
            'ProductSearchPageId': '0'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
        }
        request = FormRequest(self.product_post_url, formdata=form_data, headers=headers,
                              callback=callback, method='POST', meta=meta)

        return request

class CubusSVParseSpider(CubusParseSpider, MixinSV):
    name = MixinSV.retailer + '-parse'


class CubusSVCrawlSpider(CubusCrawlSpider, MixinSV):
    name = MixinSV.retailer + '-crawl'
    parse_spider = CubusSVParseSpider()


class CubusNOParseSpider(CubusParseSpider, MixinNO):
    name = MixinNO.retailer + '-parse'


class CubusNOCrawlSpider(CubusCrawlSpider, MixinNO):
    name = MixinNO.retailer + '-crawl'
    parse_spider = CubusNOParseSpider()
