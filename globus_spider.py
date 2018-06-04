import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from scrapy import Selector
from urllib.parse import urljoin, urlparse

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'globus-de'
    market = 'CH'
    default_brand = 'Globus'

    one_sizes = [
        'one size',
        'default'
        ]

    default_colour = ['default']

    allowed_domains = ['www.globus.ch']
    start_urls = ['https://www.globus.ch']

    listing_api_url = 'https://www.globus.ch/service/catalogue/GetFilteredCategory'
    colour_api_url = 'https://www.globus.ch/service/catalogue/GetProductDetailsWithPredefinedGroupID'
    image_url_t = 'https://www.globus.ch{}?v=gallery&width=100'


class GlobusParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    brand_css = '.mzg-catalogue-detail__product-summary__head >' \
                '.mzg-component-title_type-small ::text'
    raw_description_css = '.mzg-catalogue-detail-info__cluster-list__icons::attr(title)'
    description_re = r'description":"(.*?)","offers'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = []
        garment['skus'] = {}

        garment['gender'] = self.product_gender(garment)

        if not garment['gender']:
            garment['industry'] = 'homeware'

        garment['meta'] = {'requests_queue': self.colour_reqeusts(response)}

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('.mzg-catalogue-detail__product-summary__id::text'))[-1][:-3]

    def product_name(self, response):
        return clean(response.css('.mzg-component-title_type-page-title::text'))[0]

    def product_category(self, response):
        return clean(response.css('.mzg-components-module-breadcrumb-list ::text'))[1:-1]

    def product_description(self, response, **kwargs):
        description_script = clean(response.css('script[type="application\/ld+json"]')[1])
        description = re.findall(self.description_re, description_script)
        if description:
            return re.findall(self.description_re, description_script)[0].split(',')

    def image_urls(self, raw_product):
        return [self.image_url_t.format(image['uri']) for image in
                raw_product['galleryImages']]

    def product_gender(self, garment):
        categories = ' '.join(garment['category']).lower()
        return self.gender_lookup(categories)

    def colour_reqeusts(self, response):
        price_css = '.mzg-catalogue-detail__product-summary__productPrice small::text'
        meta = {'currency': clean(response.css(price_css))[0]}

        colour_script = clean(response.css('script[type="text/javascript"]')[-1])
        raw_data = re.findall(r'(variants":)(.*?])', colour_script)[0][1]
        product_colours = json.loads(raw_data)

        request_urls = []
        for colour in product_colours:
            meta['colour'] = colour['name']
            body = f'["{colour["id"]}","","de"]'
            request_urls.append(Request(url=self.colour_api_url, method='POST', body=body,
                        meta=meta.copy(), callback=self.parse_colours))

        return request_urls

    def parse_colours(self, response):
        garment = response.meta['garment']
        colour = response.meta['colour']
        currency = response.meta['currency']

        raw_product = json.loads(response.text)[0]
        garment['image_urls'] += self.image_urls(raw_product['product'])
        garment['skus'].update(self.skus(colour, currency, raw_product['product']))

        return self.next_request_or_garment(garment)

    def skus(self, colour, currency, raw_product):
        skus = {}

        for raw_sku in raw_product['summary']['sizes']:
            raw_prices = [
                raw_sku['price']['price'],
                raw_sku['price']['crossPrice'],
                currency
            ]

            sku = self.product_pricing_common(None, money_strs=raw_prices)

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            sku['size'] = self.one_size if raw_sku['name'].lower() in self.one_sizes else raw_sku['name']
            sku_id = sku['size']

            if colour.lower() not in self.default_colour:
                sku['colour'] = colour
                sku_id = f'{sku["colour"]}_{sku["size"]}'

            skus[sku_id] = sku

        return skus


class GlobusCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = GlobusParseSpider()

    listings_css = '#mzg-components-module-header__main-navigation'
    category_css = '.mzg-component-sidebar-navigation__list ' \
                    '.mzg-component-link.has-icon.icon-left.full-width'
    products_css = '.mzg-component-button.btn.btn-default::attr(href)'

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
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=category_css, deny=deny_re), callback='parse_category'),
    )

    def parse_category(self, response):
        meta = {'trail': self.add_trail(response)}

        raw_category_urls = clean(response.css(self.products_css))
        category_urls = [link for link in raw_category_urls
                         if not any(link.startswith(restricted_link)
                                    for restricted_link in self.deny_re)]

        for category_url in category_urls:
            yield response.follow(url=category_url, meta=meta.copy(),
                                callback=self.parse_products)

    def parse_products(self, response):
        meta = {'trail': self.add_trail(response)}

        body = f'[{{"path":"{urlparse(response.url).path}","page":1}}]'
        yield Request(url=self.listing_api_url, method='POST',
                      meta=meta.copy(),
                      body=body, callback=self.parse_pages)

    def parse_pages(self, response):
        meta = {'trail': self.add_trail(response)}
        raw_products = json.loads(response.text)[0]

        for product_detail in raw_products['items']:
            if product_detail['productSummary']['type'] == "p":
                product_url = product_detail['productSummary']['productURI']
                yield Request(url=urljoin(self.start_urls[0], product_url),
                              meta=meta.copy(),
                              callback=self.parse_item)

        if (raw_products['page'] < raw_products['pages']):
            path = raw_products['path']
            body = f'[{{"path":"{path}","page":{raw_products["page"] + 1}}}]'
            yield Request(url=self.listing_api_url, method='POST',
                          body=body, callback=self.parse_pages)

