# -*- coding: utf-8 -*-
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, Garment, clean


class Mixin(object):
    lang = 'fr'
    market = 'FR'
    retailer = 'jennyfer-fr'
    base_url = "http://www.jennyfer.com"
    allowed_domains = ['www.jennyfer.com']
    start_urls = ['http://www.jennyfer.com/']
    gender = 'women'
    brand = 'Jennyfer'


class JennyferParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = '//div[@class="pdp-top"]//span[contains(@class, "price")]//text()'

    def parse(self, response):

        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response, response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):

        sku_common = {'price': response.meta['price'],
                      'currency': response.meta['currency']}

        if response.meta['previous_prices']:
            sku_common['previous_prices'] = [response.meta['previous_prices']]

        colour = self.sku_colour(response)
        size_variations = self.sku_sizes(response)

        skus = {}
        for size in size_variations:
            sku = sku_common.copy()
            sku['colour'] = colour
            sku['size'] = size

            skus.update({colour + '_' + size: sku})

        return skus

    def colour_requests(self, response):
        css = '.variation-color .emptyswatch a::attr(href)'
        colour_links = clean(response.css(css))

        meta = {}
        meta['previous_prices'], meta['price'], meta['currency'] = self.product_pricing(response)

        return [Request(link, callback=self.parse_colour, meta=meta) for link in colour_links]

    def product_id(self, response):
        ids_array = re.findall('tc_vars\["product_id"\]\s*=\s*"(.*?)\";', response.body.decode("utf-8"))
        return (ids_array and ids_array[0]) or ""

    def image_urls(self, response):
        css = '.product-image-container .product-primary-image a::attr(href)'
        return [image for image in clean(response.css(css))]

    def product_brand(self, category):
        return self.brand

    def product_name(self, response):
        css = '#product-content .product-name::text'
        return clean(response.css(css))

    def product_category(self, response):
        css = '.breadcrumb li a span::text'
        return clean(response.css(css))

    def product_description(self, response):
        css = '.pdpForm div[itemprop="description"]::text'
        return clean(response.css(css))

    def product_care(self, response):
        css = '.pdpForm .laundry-care span::attr(title)'
        return clean(response.css(css))

    def sku_sizes(self, response):
        css = '.variation-size .emptyswatch div:not(.unselected)::text'
        return clean(response.css(css))

    def sku_colour(self, response):
        xpath = '//div[contains(@class, "variation-color")]//li[@class="emptyswatch "]' \
                '//a[child::img[@class="selected"]]//@title'
        return clean(response.xpath(xpath))[0]


class JennyferCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = JennyferParseSpider()

    allow_r = [
        '/vetements/',
        '/accessoires/',
        '/style-guide/',
    ]

    listings_css = [
        '.level-2 a',
        'div.pagination a.arrow-page',
    ]

    products_css = [
        '#search-result-items .product-wrapper > a'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item', ),
        Rule(LinkExtractor(restrict_css=listings_css, allow=allow_r), ),
    )
