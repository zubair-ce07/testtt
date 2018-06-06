import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'globus-de'
    market = 'CH'

    one_sizes = ['one size', 'default', '']

    allowed_domains = ['www.globus.ch']
    start_urls = ['https://www.globus.ch']

    colour_api_url = 'https://www.globus.ch/service/catalogue/GetProductDetailsWithPredefinedGroupID'
    image_url_t = 'https://www.globus.ch{}?v=gallery&width=100'


class GlobusParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_product = self.raw_product(response)

        if raw_product['summary']['type'] != 'p':
            return

        sku_id = self.product_id(raw_product)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['gender'] = self.product_gender(garment)
        if not garment['gender']:
            garment['industry'] = 'homeware'
        garment['image_urls'] = []
        garment['skus'] = {}

        currency = self.product_currency(response)
        garment['meta'] = {'requests_queue': self.colour_reqeusts(raw_product, currency)}

        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        raw_product = clean(response.css('script[type="text/javascript"]::text')[-1].re_first(
                r'product":(.*?),"relatedProducts'))
        return json.loads(raw_product)

    def product_id(self, raw_product):
        return raw_product['summary']['articleID']

    def product_name(self, raw_product):
        return raw_product['summary']['name']

    def product_category(self, raw_product):
        if 'paths' in raw_product:
            return [category['name'] for category in raw_product['paths'][-1]]
        else:
            return raw_product['categories']

    def product_currency(self, response):
        return {'currency': clean(response.css(
            '.mzg-catalogue-detail__product-summary__productPrice small::text'))[0]}

    def product_description(self, raw_product):
        description = []

        if 'description' in raw_product['infos']:
            for item in raw_product['infos']['description']['items']:
                if 'value' in item:
                    description.append(item['value'])
                else:
                    value = f'{item["labeledValue"]["label"]}: {item["labeledValue"]["value"]}'
                    description.append(value)
        return description

    def product_care(self, raw_product):
        care = []

        if 'care' in raw_product['infos']:
            for item in raw_product['infos']['care']['items']:
                if 'icon' in item:
                    care.append(item['icon']['label'])
                elif 'labeledValue' in item:
                    value = f'{item["labeledValue"]["label"]}: {item["labeledValue"]["value"]}'
                    care.append(value)
                else:
                    care.append(item['value'])
        return care

    def product_brand(self, raw_product):
        return raw_product['summary']['brand']['name']

    def image_urls(self, raw_product):
        return [self.image_url_t.format(image['uri']) for image in
                raw_product['product']['galleryImages']]

    def product_gender(self, garment):
        categories = ' '.join(garment['category']).lower()
        return self.gender_lookup(categories)

    def colour_reqeusts(self, raw_product, meta):
        request_urls = []

        for colour in raw_product['summary']['variants']:
            meta['colour'] = colour['name']
            body = f'["{colour["id"]}","","de"]'
            request_urls.append(Request(url=self.colour_api_url, method='POST', body=body,
                        meta=meta.copy(), callback=self.parse_colours))

        return request_urls

    def parse_colours(self, response):
        garment = response.meta['garment']

        raw_product = json.loads(response.text)[0]
        garment['image_urls'] += self.image_urls(raw_product)
        garment['skus'].update(self.skus(raw_product, response))

        return self.next_request_or_garment(garment)

    def skus(self, raw_product, response):
        skus = {}

        colour = response.meta['colour']
        currency = response.meta['currency']

        for raw_sku in raw_product['product']['summary']['sizes']:
            money_strs = [
                raw_sku['price']['price'],
                raw_sku['price']['crossPrice'],
                currency
            ]

            sku = self.product_pricing_common(None, money_strs=money_strs)

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            sku['size'] = sku_id = (self.one_size
                                    if raw_sku['name'].lower() in self.one_sizes
                                    else raw_sku['name'])

            if colour.lower() != 'default':
                sku['colour'] = colour
                sku_id = f'{sku["colour"]}_{sku["size"]}'

            skus[sku_id] = sku

        return skus


class GlobusCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = GlobusParseSpider()

    listings_css = [
        '#mzg-components-module-header__main-navigation',
        '.mzg-component-button.btn.btn-default',
        'link[rel="next"]'
        ]

    products_css = '.mzg-components-module-product-listing__column'

    deny_re = [
        '/home-living/kueche/kuechenmaschinen-zubehoer',
        '/home-living/elektronik-gadgets',
        '/home-living/yoga/yoga',
        '/home-living/outdoor/velo',
        '/kinder/spielwaren',
        '/delicatessa',
        '/wein-drinks'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re, tags=['link', 'a']), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny_re), callback='parse_item'),
    )

