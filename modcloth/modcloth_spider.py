import json
import re
from w3lib.url import url_query_cleaner

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    market = 'US'
    gender = Gender.WOMEN.value
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
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.product_colour_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour_requests(self, response):
        garment = response.meta['garment']
        urls = clean(response.css('.thumb img::attr(src)'))
        garment['image_urls'] += [url_query_cleaner(u) for u in urls]
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('input[name="pid"]::attr(value)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumb-element::text'))[:-1]

    def skus(self, response):
        raw_skus = clean(response.css('script:contains("mc_global.product")::text'))[0]
        raw_skus = json.loads(re.findall(r'\[.*\]', raw_skus)[0])
        raw_sku = next(rs for rs in raw_skus if rs['variationGroupID'] == self.product_id(response))

        skus = {}
        colour = self.product_colour(response)
        common_sku = self.product_pricing_common(response)

        for raw_size in raw_sku['product_variants']:
            sku = common_sku.copy()
            sku['colour'] = colour
            sku['size'] = raw_size['size']
            sku['out_of_stock'] = not raw_size['units_available'] or raw_sku['archived']
            skus[raw_size['upc']] = sku

        return skus

    def product_colour(self, response):
        return clean(response.css('.swatches.color .selected img::attr(alt)'))[0]

    def product_colour_requests(self, response):
        urls = clean(response.css('.swatches.color a::attr(href)'))
        return [Request(url=url, callback=self.parse_colour_requests) for url in urls]


class ModClothCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ModClothParseSpider()

    listings_css = ['.menu-category', '.page-next']
    products_css = ['.thumb-link']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
