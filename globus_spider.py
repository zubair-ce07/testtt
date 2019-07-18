import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'globus-ch'
    market = 'CH'
    default_brand = 'Globus'

    allowed_domains = ['globus.ch']
    start_urls = ['https://www.globus.ch']

    def raw_product(self, response):
        product_re = '__NEXT_DATA__ = (.*);__NEXT_LOADED'
        return json.loads(response.css('script::text').re_first(product_re))


class GlobusParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    raw_description_css = '.mzg-catalogue-detail-info span::text'
    price_css = '.mzg-catalogue-detail__product-summary__productPrice *::text'

    image_url_t = 'https://www.globus.ch{}.webp?v=gallery&width=500'

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(raw_product)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response, raw_product)

        garment['meta'] = {
            'requests_queue': self.colour_requests(response, raw_product)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        raw_product = response.meta['raw_product']
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response, raw_product))

        return self.next_request_or_garment(garment)

    def colour_requests(self, response, raw_product):
        raw_variants = raw_product['props']['initialStoreState']['detail']['product']['summary']['variants']
        item_url = response.url.rsplit('-', 1)[0]

        requests = []

        for raw_variant in raw_variants:
            if raw_variant['id'].lower() not in response.url:
                sku_url = f'{item_url}-{raw_variant["id"].lower()}'
                requests.append(Request(url=sku_url, callback=self.parse_colour, meta={'raw_product': raw_product}))

        return requests

    def skus(self, response, raw_product):
        colour_css = '.mzg-catalogue-detail__product-summary__variant-select ' \
                     '.mzg-component-title_type-small ::text'

        skus = {}

        raw_colour = clean(response.css(colour_css))
        common_sku = {'colour': raw_colour[0].split(': ')[1]} if raw_colour else {}

        raw_skus = raw_product['props']['initialStoreState']['detail']['product']['summary']['sizes']

        for raw_sku in raw_skus:
            sku = common_sku.copy()

            sku['size'] = raw_sku['value'] if sku.get('value') else self.one_size
            sku.update(self.product_pricing_common(response))

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            skus[raw_sku['sku']] = sku

        return skus

    def product_id(self, raw_product):
        return raw_product['props']['initialStoreState']['detail']['product']['id']

    def product_name(self, response):
        css = '.mzg-component-title_type-page-title ::text, mzg-component-title_type-normal ::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = r'script[type=application\/ld\+json]::text'
        raw_category = json.loads(clean(response.css(css))[0])

        return [raw_c['item']['name'] for raw_c in raw_category['itemListElement']]

    def product_gender(self, response):
        raw_gender = soupify(self.product_category(response))
        return self.gender_lookup(raw_gender) or Gender.ADULTS.value

    def image_urls(self, raw_product):
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

    listings_css = ['.mzg-component-main-navigation__item', '.mzg-element__teaser']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        yield from super().parse(response)
        raw_pagination = self.raw_product(response)

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
