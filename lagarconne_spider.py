import json

from scrapy.http import Response
from scrapy.spiders import Rule
from scrapy.selector import Selector

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'lagarconne'
    allowed_domains = ['lagarconne.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'

    start_urls = ['https://lagarconne.com']
    one_size_label = 'one size'


class LaGarconneParseSpider(BaseParseSpider):
    price_css = '[itemprop="price"] .money::text'
    raw_description_css = '.lg-desc-product p::text'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate(garment, response)
        raw_product = self.raw_product(response)
        garment['care'] = self.product_care(response)
        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(raw_product)
        garment['category'] = self.product_category(garment)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['description'] = self.product_description(response)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(response)

        if self.out_of_stock(response, response):
            return garment

        requests = self.colour_requests(response, raw_product)
        garment['skus'] = self.skus(response, raw_product)
        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        raw_product = self.raw_product(response)

        garment['skus'].update(self.skus(response, raw_product))
        garment['image_urls'] += self.image_urls(raw_product)

        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        css = 'script:contains("productJSON")::text'
        return json.loads(response.css(css).re('{.*}')[0])

    def out_of_stock(self, hxs, response):
        css = '.lg-product-details:contains("SOLD OUT"), .lg-product-details:contains("Call to Order")'
        return response.css(css)

    def product_id(self, response):
        return clean(response.css('.product_id::text'))[0][:6]

    def product_category(self, garment):
        if isinstance(garment, Response):
            return
        if garment['trail']:
            return clean([x[0].upper() for x in garment['trail'] if x[0]])

    def product_name(self, raw_product):
        return raw_product['title']

    def product_brand(self, raw_product):
        return raw_product['vendor']

    def image_urls(self, raw_product):
        return raw_product['images']

    def skus(self, response, raw_product):
        skus = {}
        previous_price = raw_product['compare_at_price']
        common_sku = self.product_pricing_common(response, money_strs=[previous_price])
        common_sku['color'] = self.detect_colour(raw_product['description'])
        for raw_sku in raw_product['variants']:
            sku = common_sku.copy()

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            size = raw_sku['option1']
            sku['size'] = self.one_size if size.lower() in self.one_size_label else size

            skus[raw_sku['sku']] = sku

        return skus

    def colour_requests(self, response, raw_product):
        css = '#availablecolors ::attr(href)'
        colour_s = Selector(text=raw_product['description'])
        return [response.follow(u, callback=self.parse_colour) for u in clean(colour_s.css(css))]

    def is_homeware(self, response):
        if 'interiors' in response.url:
            return True
        return False

    def product_gender(self, response):
        return response.meta.get('gender')


class LaGarconneCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.lg-filter-list-desktop',
        '.pagination'
    ]

    products_css = '.lg-product-list-item'

    deny = '/pages'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny), callback='parse_item')
    )


class LaGarconneParseSpiderUS(LaGarconneParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class LaGarconneCrawlSpiderUS(LaGarconneCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = LaGarconneParseSpiderUS()
