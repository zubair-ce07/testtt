import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'globus-ch'
    market = 'CH'
    default_brand = 'Globus'

    allowed_domains = ['globus.ch']
    start_urls = ['https://www.globus.ch']


class GlobusParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    raw_description_css = '.mzg-catalogue-detail-info span::text'

    image_url_t = 'https://www.globus.ch{}.webp?v=gallery&width=500'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment["gender"] = self.product_gender(response)
        garment["skus"] = self.skus(response)

        garment['meta'] = {
            'requests_queue': self.colour_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        raw_product = self.raw_product(response)
        raw_variants = raw_product['props']['initialStoreState']['detail']['product']['summary']['variants']
        item_url = response.url.rsplit('-', 1)[0]

        requests = []

        for raw_variant in raw_variants:
            if raw_variant["id"].lower() not in response.url:
                sku_url = f'{item_url}-{raw_variant["id"].lower()}'
                requests.append(Request(url=sku_url, callback=self.parse_colour))

        return requests

    def skus(self, response):
        raw_product = self.raw_product(response)
        colour_css = '.mzg-catalogue-detail__product-summary__variant-select ' \
                     '.mzg-component-title_type-small ::text'

        skus = {}
        common_sku = {}

        raw_colour = clean(response.css(colour_css))
        raw_skus = raw_product['props']['initialStoreState']['detail']['product']['summary']['sizes']

        if raw_colour:
            common_sku['colour'] = self.detect_colour(raw_colour[0])

        common_sku['currency'] = clean(response.css('.mzg-component-price small ::text'))[0]

        for raw_sku in raw_skus:
            sku = common_sku.copy()

            sku['size'] = raw_sku['value'] if sku.get('value') else self.one_size
            sku.update(self.pricing(raw_sku))

            if not raw_sku["available"]:
                sku["out_of_stock"] = True

            skus[raw_sku['sku']] = sku

        return skus

    def pricing(self, raw_sku):
        pricing = {}
        raw_prices = raw_sku['price']

        pricing['price'] = raw_prices['price']

        if raw_prices.get('crossPrice'):
            pricing['previous_prices'] = [raw_sku['price']['crossPrice']]

        return pricing

    def raw_product(self, response):
        product_re = '__NEXT_DATA__ = (.*);__NEXT_LOADED'
        return json.loads(response.css('script::text').re_first(product_re))

    def product_id(self, response):
        raw_product = self.raw_product(response)
        return raw_product['props']['initialStoreState']['detail']['product']['id']

    def product_name(self, response):
        css = '.mzg-component-title_type-page-title ::text, mzg-component-title_type-normal ::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = r'script[type=application\/ld\+json]::text'
        raw_category = json.loads(clean(response.css(css))[0])

        return [raw_c['item']['name'] for raw_c in raw_category['itemListElement']]

    def product_gender(self, response):
        soup = ' '.join(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        raw_product = self.raw_product(response)
        raw_images = raw_product['props']['initialStoreState']['detail']['product']

        image_urls = []

        for raw_image in raw_images['galleryImages']:
            self.image_url_t.format(raw_image['uri'])
            image_urls.append(self.image_url_t.format(raw_image['uri']))

        return image_urls


class GlobusCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = GlobusParseSpider()

    pagination_url = 'https://www.globus.ch/service/catalogue/GetFilteredCategory'

    category_css = '.mzg-component-main-navigation__item'
    sub_category_css = '.mzg-element__teaser'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=sub_category_css), callback='parse_pagination'),
    )
    
    def parse_pagination(self, response):
        yield Request(url=response.url, callback=self.parse)
        raw_pagination = self.parse_spider.raw_product(response)

        if raw_pagination['props']['initialStoreState'].get('category'):
            raw_category = raw_pagination['props']['initialStoreState']['category']

            total_pages = raw_category['listing']['pages']
            payload = {
                'path': raw_category['listing']['path'],
                'sort': raw_category['listing']['selectedSorting'],
                'pageSize': str(raw_category['listing']['pageSize']),
            }

            for page in range(total_pages):
                payload['page'] = str(page + 1)
                yield Request(self.pagination_url, self.parse_category, method='POST', body=json.dumps([payload]))

    def parse_category(self, response):
        raw_category = json.loads(response.text)
        raw_items = raw_category[0]['items']

        for raw_item in raw_items:
            yield response.follow(raw_item['productSummary']['productURI'], callback=self.parse_item)
