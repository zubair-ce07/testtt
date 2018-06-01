import json
import re

from scrapy import Request
from scrapy import Selector
from urllib.parse import urlparse, urljoin

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'globus-de'
    market = 'DE'
    default_brand = 'Globus'
    retailer_currency = 'CHF'

    gender_map = [
        ("herren", Gender.MEN.value),
        ("damen", Gender.WOMEN.value),
        ("kinder", Gender.KIDS.value),
        ]

    one_sizes = [
        'one size',
        'default'
        ]

    default_colour = ['default']

    allowed_domains = ['www.globus.ch']

    base_url = 'https://www.globus.ch'
    category_api_url = 'https://www.globus.ch/service/site/GetFlyoutNavigation'
    linting_api_url = 'https://www.globus.ch/service/catalogue/GetFilteredCategory'
    variant_api_url = 'https://www.globus.ch/service/catalogue/GetProductDetailsWithPredefinedGroupID'


class GlobusParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    colour_map = {}

    brand_css = '.mzg-catalogue-detail__product-summary__head >' \
                '.mzg-component-title_type-small ::text'
    description_css = '.mzg-catalogue-detail-info__cluster-list >' \
                      '.mzg-catalogue-detail-info__cluster-list__item ::text'
    raw_description_css = '.mzg-catalogue-detail-info__cluster-list__icons::attr(title)'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = []
        garment['skus'] = {}

        garment['gender'] = self.product_gender(garment)
        garment['description'] = self.product_description(response)

        if not garment['gender']:
            garment['industry'] = 'homeware'

        garment['meta'] = {'requests_queue': self.variant_requests(response)}

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('.mzg-catalogue-detail__product-summary__id::text'))[-1][:-3]

    def product_name(self, response):
        return clean(response.css('.mzg-component-title_type-page-title::text'))[0]

    def product_category(self, response):
        return clean(response.css('.mzg-components-module-breadcrumb-list ::text'))[1:-1]

    def product_description(self, response, **kwargs):
        description = []

        raw_description = clean(response.css(self.description_css))
        raw_description = self.care_detector.split_and_filter(strs=raw_description)
        raw_strs = self.raw_description(response, **kwargs)
        raw_description = raw_description + [rd for rd in raw_strs if not self.care_criteria(rd)]

        for index, value in enumerate(raw_description):
            if index > 0 and raw_description[index-1] == ":":
                delimeter = description.pop()
                item = description.pop()
                item += delimeter + value
                description.append(item)
            else:
                description.append(value)

        return description

    def image_urls(self, raw_product):
        image_urls = []
        for image in raw_product['galleryImages']:
            image_urls.append(urljoin(self.base_url, image['uri'] + '?v=gallery&width=100'))

        return image_urls

    def product_gender(self, garment):
        categories = ' '.join(garment['category']).lower()
        for gender_str, gender in self.gender_map:
            if gender_str in categories:
                return gender

        return None

    def variant_requests(self, response):
        raw_data = re.findall(r'(variants":)(.*?])', response.text)[0][1]
        product_colours = json.loads(raw_data)

        request_urls = []
        for colour in product_colours:
            colour_id = colour["id"]

            self.colour_map.update({colour_id: colour['name']})

            body = f'["{colour_id}","","de"]'
            request_urls.append(Request(url=self.variant_api_url, method='POST', body=body,
                        callback=self.parse_variant))

        return request_urls

    def parse_variant(self, response):
        garment = response.meta['garment']

        raw_product = json.loads(response.text)[0]
        garment['image_urls'] += self.image_urls(raw_product['product'])
        garment['skus'].update(self.skus(raw_product['product']))

        return self.next_request_or_garment(garment)

    def skus(self, raw_product):
        skus = {}
        colour = self.colour_map.get(raw_product['id'])

        for raw_sku in raw_product['summary']['sizes']:
            raw_prices = []
            raw_prices.extend((raw_sku['price']['price'], raw_sku['price']['crossPrice']))

            sku = self.product_pricing_common(None, money_strs=raw_prices)

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            if not sku['currency']:
                sku['currency'] = self.retailer_currency

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

    restricted_links = [
        '/home-living/kueche/kuechenmaschinen-zubehoer',
        '/home-living/elektronik-gadgets',
        '/home-living/yoga/yoga',
        '/home-living/outdoor/velo',
        '/kinder/spielwaren',
        '/delicatessa',
        '/wein-drinks'
        ]

    category_re = r'"flyoutReference":"(.*?)"'
    listing_css = '.mzg-component-link::attr(href)'

    def start_requests(self):
        yield Request(url=self.base_url, callback=self.parse_category)

    def parse_category(self, response):
        meta = {'trail': self.add_trail(response)}
        category_ids = re.findall(self.category_re, response.text)
        for category_id in category_ids:
            body = f'["{category_id}", "de"]'
            yield Request(url=self.category_api_url, method='POST', body=body,
                          meta=meta.copy(),
                          callback=self.parse_listing)

    def parse_listing(self, response):
        meta = {'trail': self.add_trail(response)}
        raw_listing = Selector(text=json.loads(response.body)[0])

        raw_urls = clean(raw_listing.css(self.listing_css))
        product_urls = [url for url in raw_urls
                          if not any(url.startswith(restricted_link)
                            for restricted_link in self.restricted_links)]

        for product_url in product_urls:
            body = f'[{{"path":"{product_url}","page":1}}]'
            yield Request(url=self.linting_api_url, method='POST',
                          meta=meta.copy(),
                          body=body, callback=self.parse_pages)

    def parse_pages(self, response):
        meta = {'trail': self.add_trail(response)}
        raw_products = json.loads(response.text)[0]

        for product_detail in raw_products['items']:
            if product_detail['productSummary']['type'] == "p":
                product_url = product_detail['productSummary']['productURI']
                yield Request(url=urljoin(self.base_url, product_url),
                              meta=meta.copy(),
                              callback=self.parse_item)

        if (raw_products['page'] < raw_products['pages']):
            body = f'[{{"path":"{product_url}","page":{raw_products["page"] + 1}}}]'
            yield Request(url=self.linting_api_url, method='POST',
                          body=body, callback=self.parse_pages)

