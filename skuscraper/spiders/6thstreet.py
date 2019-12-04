import json

from scrapy import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify


class Mixin:
    retailer = '6thstreet'


class MixinAE(Mixin):
    market = 'AE'
    retailer = Mixin.retailer + '-ae'
    allowed_domains = ['6thstreet.com', '02x7u6o3si-dsn.algolia.net']
    start_urls = [
        'https://en-ae.6thstreet.com/women.html'
    ]


class SixthStreetSpider(BaseParseSpider):

    def parse(self, response):
        raw_product = response.meta['product']
        pid = raw_product['sku']

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate(garment, response)
        garment['trail'] = response.meta['trail']
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(response)
        garment['category'] = self.product_category(raw_product['categories']['level2'][0])
        garment['brand'] = self.product_brand(raw_product)
        garment['image_urls'] = self.product_images(raw_product)
        garment['gender'] = self.product_gender(response, raw_product)
        garment['skus'] = self.product_skus(response, raw_product)
        return garment

    def product_retailer_sku(self, response):
        raw_retailer_sku = response.css('.pdp_middle_right li span')[1]
        return clean(raw_retailer_sku)

    def product_name(self, response):
        raw_name = response.css('.product_name::text').get()
        return clean(raw_name)

    def product_description(self, raw_data):
        return [raw_data['description']]

    def product_category(self, raw_data):
        return raw_data.split(' /// ')

    def product_brand(self, raw_data):
        return clean(raw_data['brand_name'])

    def product_images(self, raw_data):
        return raw_data['gallery_images']

    def product_gender(self, response, raw_data):
        soup = soupify(raw_data['gender'])
        gender = self.gender_lookup(soup, merge_genders=True)
        return gender

    def product_skus(self, response, raw_product):
        sizes_us = raw_product['size_us']
        sizes_uk = raw_product['size_uk']
        sizes_eu = raw_product['size_eu']

        common_sku = self.product_price(raw_product['price'][0])
        common_sku['colour'] = raw_product['color']

        if not sizes_us:
            common_sku['size'] = 'One'
            return {'One': common_sku}

        skus = {}
        for size_us, size_uk, size_eu in zip(sizes_us, sizes_uk, sizes_eu):
            sku = common_sku.copy()
            size = f'US_{size_us}/UK_{size_uk}/EU_{size_eu}'
            sku['size'] = size
            skus[size] = sku

        return skus

    def product_price(self, raw_data):
        currency = list(raw_data.keys())[0]
        return {
            'price': int(raw_data[currency]['default']),
            'currency': currency,
            'previous_prices': [raw_data[currency]['6s_base_price']],
        }


class SixthStreetCrawler(BaseCrawlSpider):
    url = 'https://02x7u6o3si-dsn.algolia.net/1/indexes/*/queries?'
    allow = r'.html'
    listings_css = [
        '.third-level-sub'
    ]

    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listings_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        raw_data = response.css('[crossorigin="anonymous"] + script::text').re_first('=\s*({.*})')
        raw_data = json.loads(raw_data)
        query = raw_data.get('request')['path'].replace('///', '')
        body = self.make_request_body(query)
        url = add_or_replace_parameter(self.url, 'x-algolia-application-id', raw_data.get('applicationId'))
        url = add_or_replace_parameter(url, 'x-algolia-api-key', raw_data.get('apiKey'))

        yield FormRequest(url=url, body=json.dumps(body), method='POST', callback=self.parse_products,
                          meta={'trail': self.add_trail(response)})

    def parse_products(self, response):
        raw_data = json.loads(response.text)
        products = raw_data['results'][0]['hits']

        for product in products:
            yield Request(url=product['url'], callback=self.parse_item, meta={'product': product,
                                                                              'trail': self.add_trail(response)})

        current_page = raw_data['results'][0]['page']
        total_pages = raw_data['results'][0]['nbPages']

        if current_page < total_pages:
            query = raw_data['results'][0]['query']
            body = self.make_request_body(query, current_page+1)
            yield FormRequest(url=response.url, body=json.dumps(body), method='POST', callback=self.parse_products)

    def make_request_body(self, query, page_num=0):
        return {"requests": [{"indexName": "enterprise_magento_english_products",
                              "params": f"query={query}&hitsPerPage=60&maxValuesPerFacet=60&page={page_num}"}
                             ]}


class SixthStreetAESpider(MixinAE, SixthStreetSpider):
    name = MixinAE.retailer + '-parse'


class SixthStreetAECrawler(MixinAE, SixthStreetCrawler):
    name = MixinAE.retailer + '-crawl'
    parse_spider = SixthStreetAESpider()
