import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'globus-de'
    market = 'CH'
    default_brand = 'Globus'

    one_sizes = [
        'one size',
        'default',
        ''
        ]

    default_colour = ['default']

    allowed_domains = ['www.globus.ch']
    start_urls = ['https://www.globus.ch']

    colour_api_url = 'https://www.globus.ch/service/catalogue/GetProductDetailsWithPredefinedGroupID'
    image_url_t = 'https://www.globus.ch{}?v=gallery&width=100'


class GlobusParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        raw_data = clean(response.css('script[type="text/javascript"]::text')[-1])
        raw_details = re.findall(r'product":(.*?),"relatedProducts', raw_data)[0]
        product = json.loads(raw_details)
        if product['summary']['type'] != 'p':
            return

        sku_id = self.product_id(product)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(product)
        garment['description'] = self.product_description(product)
        garment['care'] = self.product_care(product)
        garment['category'] = self.product_category(product)
        garment['brand'] = self.product_brand(product)
        garment['gender'] = self.product_gender(garment)
        if not garment['gender']:
            garment['industry'] = 'homeware'

        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colour_reqeusts(
                                                product,
                                                self.product_currency(response))}

        return self.next_request_or_garment(garment)

    def product_id(self, product):
        return product['summary']['articleID']

    def product_name(self, product):
        return product['summary']['name']

    def product_category(self, product):
        return [category['name'] for category in product['paths'][-1]]

    def product_currency(self, response):
        price_css = '.mzg-catalogue-detail__product-summary__productPrice small::text'
        return {'currency': clean(response.css(price_css))[0]}

    def product_description(self, product, **kwargs):
        if 'description' in product['infos']:
            return [item['value']
                    if 'value' in item
                    else f'{item["labeledValue"]["label"]}: {item["labeledValue"]["value"]}'
                    for item in product['infos']['description']['items']]
        else:
            return ['no description']

    def product_care(self, product, **kwargs):
        if 'care' in product['infos']:
            return [item['icon']['label']
                    if 'icon' in item
                    else f'{item["labeledValue"]["label"]}: {item["labeledValue"]["value"]}'
                    if 'labeledValue' in item
                    else item['value']
                    for item in product['infos']['care']['items']]
        else:
            return ['no care']

    def product_brand(self, product):
        return product['summary']['brand']['name']

    def image_urls(self, product):
        return [self.image_url_t.format(image['uri']) for image in
                product['product']['galleryImages']]

    def product_gender(self, garment):
        categories = ' '.join(garment['category']).lower()
        return self.gender_lookup(categories)

    def colour_reqeusts(self, product, meta):
        request_urls = []

        for colour in product['summary']['variants']:
            meta['colour'] = colour['name']
            body = f'["{colour["id"]}","","de"]'
            request_urls.append(Request(url=self.colour_api_url, method='POST', body=body,
                        meta=meta.copy(), callback=self.parse_colours))

        return request_urls

    def parse_colours(self, response):
        garment = response.meta['garment']

        product = json.loads(response.text)[0]
        garment['image_urls'] += self.image_urls(product)
        garment['skus'].update(self.skus(product, response))

        return self.next_request_or_garment(garment)

    def skus(self, product, response):
        skus = {}

        colour = response.meta['colour']
        currency = response.meta['currency']

        for raw_sku in product['product']['summary']['sizes']:
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

            if colour.lower() not in self.default_colour:
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

