import json
import re
from w3lib.url import url_query_cleaner

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    market = 'US'
    gender = 'women'
    default_brand = 'ModCloth'
    retailer = 'modcloth-us'

    allowed_domains = ['modcloth.com']
    start_urls = ['https://www.modcloth.com/']


class ModClothParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = '.product-info .tab-content:last-child ::text'
    care_css = '.product-main-attributes .value::text'
    brand_css = '.mobile-only .product-brand a::text'
    price_css = '.product-price ::text'

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = Mixin.gender
        garment['skus'] = self.skus(response)
        garment['meta'] = {
            'requests_queue': self.image_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        urls = clean(response.css('.thumb img::attr(src)').getall())
        garment['image_urls'] = garment.get('image_urls', []) + [url_query_cleaner(u) for u in urls]

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.css('input[name="pid"]::attr(value)').get()

    def product_name(self, response):
        return response.css('.product-name::text').get()

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text').getall())

    def skus(self, response):
        raw_skus = clean(response.css('script:contains("mc_global.product")::text'))[0]
        raw_skus = json.loads(re.findall(r'\[.*\]', raw_skus)[0])
        pricing = self.product_pricing_common(response)
        skus = {}

        for raw_sku in raw_skus:
            colour = self.detect_colour(raw_sku['url'])
            for raw_size in raw_sku['product_variants']:
                sku = pricing.copy()
                sku['colour'] = colour
                sku['size'] = raw_size['size']
                sku['out_of_stock'] = not(raw_size['units_available']) or raw_sku['archived']
                skus[raw_size['upc']] = sku

        return skus

    def image_requests(self, response):
        urls = response.css('.swatches.color a::attr(href)').getall()
        return [Request(url=url, callback=self.parse_image_urls) for url in urls]


class ModClothCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ModClothParseSpider()

    listings_css = ['.menu-category', '.page-next']
    products_css = ['.thumb-link']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
