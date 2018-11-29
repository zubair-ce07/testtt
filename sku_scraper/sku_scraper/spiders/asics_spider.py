import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.selector import Selector

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'asics-au'
    market = 'AU'

    allowed_domains = ['asics.com']
    start_urls = ['https://www.asics.com/au/en-au/']


class AsicsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    default_brand = 'Asics'

    price_css = 'span[itemprop="offers"]::text'
    brand_css = '[itemprop="brand"]::attr(content)'
    raw_description_css = '#collapse1 ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if self.out_of_stock(response):
            return self.out_of_stock_item(response, response, product_id)

        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        css = ':not(.active) > .colorVariant::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colour) for url in urls]

    def out_of_stock(self, response):
        return clean(response.css('.title'))

    def product_id(self, response):
        return response.url.split('/')[-1].split('.')[0]

    def product_name(self, response):
        return clean(response.css('[property="og:title"]::attr(content)'))[0]

    def product_category(self, response):
        css = '#promotion-container ::text, .breadcrumb a::text'
        return clean(response.css(css))

    def image_urls(self, response):
        return clean(response.css('#pdp-main-image ::attr(data-url-src)'))

    def product_gender(self, response):
        soup = soupify(clean(response.css('#unisex-tab::attr(class)')))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        skus = {}

        common_sku = self.product_pricing_common(response)
        if response.css('.out-of-stock'):
            common_sku['out_of_stock'] = True

        common_sku['colour'] = clean(response.css('[itemprop="color"]::text'))[0]

        raw_product = clean(response.css('[type="text/javascript"]::text'))[0]
        raw_product = json.loads(re.search('{"p(.*)D"}', raw_product).group(0))

        for size, availability in raw_product['product']['stock-size'].items():
            sku = common_sku.copy()
            if availability.lower() == 'no':
                sku['out_of_stock'] = True
            sku['size'] = self.one_size if size == 'OS' else size

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus


class AsicsCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = AsicsParseSpider()

    listings_css = ['.nav-menu', '.pagination']
    products_css = ['.productMainLink']

    deny_listings = ['tiger']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_listings), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
