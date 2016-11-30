# -*- coding: utf-8 -*-
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider
from .base import BaseCrawlSpider
from .base import Garment
from .base import clean
import pdb


class Mixin(object):
    lang = 'fr'
    market = 'FR'
    retailer = 'jennyfer-fr'
    base_url = "http://www.jennyfer.com"
    allowed_domains = ['www.jennyfer.com']
    start_urls = ['http://www.jennyfer.com/']


class JennyferParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = '//div[@class="pdp-top"]//span[contains(@class, "price")]//text()'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response, response)
        garment['gender'] = 'women'

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.color_requests(response)}

        return self.next_request_or_garment(garment)

    def color_requests(self, response):
        xpath = '//div[contains(@class, "variation-color")]//li[@class="emptyswatch "]//a//@href'
        color_links = clean(response.xpath(xpath))

        meta = {}
        meta['previous_prices'], meta['price'], meta['currency'] = self.product_pricing(response)

        return [Request(link, callback=self.parse_skus, meta=meta) for link in color_links]

    def parse_skus(self, response):
        garment = response.meta['garment']

        # each color has its own separate images on each page
        garment['image_urls'] += self.image_urls(response)

        sku_common = {'price': response.meta['price'],
                      'currency': response.meta['currency']}

        if response.meta['previous_prices']:
            sku_common['previous_prices'] = [response.meta['previous_prices']]

        color = self.get_product_color(response)
        size_variations = self.get_available_sizes(response)

        for size in size_variations:
            sku = sku_common.copy()
            sku['color'] = color
            sku['size'] = size
            garment['skus'][sku['color'] + '_' + size] = sku

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        ids_array = re.findall('tc_vars\["product_id"\]\s*=\s*"(.*?)\";', response.body.decode("utf-8"))
        return (ids_array and ids_array[0]) or ""

    def image_urls(self, response):
        xpath = "//div[@class='product-image-container']//div[@class='product-primary-image']//a/@href"
        return [image for image in clean(response.xpath(xpath))]

    def product_brand(self, category):
        return 'Jennyfer'

    def product_name(self, response):
        xpath = '//div[@id="product-content"]//h1[@class="product-name"]//text()'
        return clean(response.xpath(xpath))[0]

    def product_category(self, response):
        xpath = '//ol[@class="breadcrumb"]//li//a//span//text()'
        return clean(response.xpath(xpath))

    def product_description(self, response):
        xpath = '//form[@class="pdpForm"]//div[@itemprop="description"]//text()'
        return clean(response.xpath(xpath))

    def product_care(self, response):
        xpath = '//form[@class="pdpForm"]//div[@class="laundry-care"]//span//@title'
        return clean(response.xpath(xpath))

    def product_pricing(self, response):
        return self.extract_prices(response, self.price_x)

    def get_available_sizes(self, response):
        xpath = '//div[contains(@class, "variation-size")]//li[@class="emptyswatch "]' \
                '//div[not(contains(@class, "unselected"))]//text()'
        return clean(response.xpath(xpath))

    def get_product_color(self, response):
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

    listings_x = [
        '.menu-category li .level-2 a.level-2'
    ]

    products_x = [
        '#search-result-items .list-tile .product-wrapper > a'
    ]

    pagination_x = [
        'div.pagination a.arrow-page'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_css=products_x, deny=()), callback='parse_item',),
        Rule(LinkExtractor(restrict_css=listings_x, allow=allow_r), callback='parse_pagination',),
    )

    def parse_pagination(self, response):
        product_links = LinkExtractor(restrict_css=self.products_x).extract_links(response)
        for link in product_links:
            yield Request(link.url, meta={'trail': self.add_trail(response)}, callback=self.parse_item)

        next_page = LinkExtractor(restrict_css=self.pagination_x).extract_links(response)
        if next_page:
            yield Request(next_page[-1].url, callback=self.parse_pagination)
