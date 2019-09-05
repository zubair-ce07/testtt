import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = 'lululemon'
    default_brand = 'Lululemon'
    spider_one_sizes = ['One Size']


class MixinEU(Mixin):
    retailer = Mixin.retailer + '-eu'
    market = 'EU'
    allowed_domains = ['eu.lululemon.com']
    start_urls = [
        'https://www.eu.lululemon.com/en-lu/home'
    ]
    sku_request_t = 'https://www.eu.lululemon.com/on/demandware.store/Site' \
                    's-EU-Site/en_LU/Product-Variation'


class ParseSpider(BaseParseSpider):
    description_css = '.fabric-description ::text'
    care_css = '.product-care ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['care'] = self.product_care(response)
        garment['skus'] = {}
        garment['image_urls'] = []
        requests = self.color_requests(response, product_id)
        garment['meta'] = {
            'requests_queue': requests
        }
        return self.next_request_or_garment(garment)

    def color_requests(self, response, product_id):
        color_ids = response.css('.pdp-swatches .selectable::attr(data-attr-value)').getall()
        size_ids = response.css('.select-size ::attr(data-attr-value)').getall()
        return [self.sku_request_params(color_id, size_id, product_id)
                for color_id in color_ids for size_id in size_ids]

    def sku_request_params(self, color_id, size_id, product_id):
        params = {
            f'dwvar_prod{product_id}_color': color_id,
            f'dwvar_prod{size_id}_size': size_id,
            'pid': product_id,
            'quantity': 1
        }
        request_url = add_or_replace_parameters(self.sku_request_t, params)
        return Request(request_url, callback=self.parse_color)

    def parse_color(self, response):
        raw_product = json.loads(response.text)
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(raw_product)
        garment['skus'].update(self.parse_sku(raw_product))
        return self.next_request_or_garment(garment)

    def image_urls(self, raw_product):
        images = raw_product['product']['images']['hi-res']
        return [image['url'] for image in images]

    def parse_sku(self, raw_product):
        skus = {}
        sku = {
            'price': raw_product['product']['price']['sales']['value'],
            'currency': raw_product['product']['price']['sales']['currency'],
            'size': raw_product['digitalProductData']['size']
        }

        colors = raw_product['product']['variationAttributes'][0]['values']
        for color in colors:
            if color['selected']:
                sku['colour'] = color['displayValue']
                break

        previous_price = raw_product['product']['price'].get('list')
        if previous_price:
            sku['previous_price'] = previous_price['value']

        if not raw_product['product']['available']:
            sku['out_of_stock'] = True

        skus[f'{sku["colour"]}_{sku["size"]}'] = sku
        return skus

    def product_id(self, response):
        return clean(response.css('.product-id::text'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name::text'))[0]

    def product_category(self, response):
        raw_category_css = 'script:contains(unifiedID)'
        regex = 'unifiedID\"\:\"(.+?)\"'
        return response.css(raw_category_css).re_first(regex).split('-')

    def product_gender(self, response):
        soup = clean(response.css('script:contains(gender) ::text'))[0]
        return self.gender_lookup(soup) or Gender.ADULTS.value


class CrawlSpider(BaseCrawlSpider):
    listings_css = ['#category-accordion-container']
    product_css = ['.image-container a:first-of-type']
    deny = ['the-sweatlife', 'my-account', 'login', 'countries-europe']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_pagination(self, response):
        yield from self.parse(response)

        next_page_url = response.css('.btn-primary ::attr(data-url)').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_pagination)

    def parse_item(self, response):
        yield from self.parse_spider.parse(response)


class ParseSpiderDE(MixinEU, ParseSpider):
    name = MixinEU.retailer + '-parse'


class CrawlSpiderDE(MixinEU, CrawlSpider):
    name = MixinEU.retailer + '-crawl'
    parse_spider = ParseSpiderDE()
