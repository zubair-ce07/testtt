from copy import deepcopy

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'liujo-it'
    market = 'IT'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb/']
    gender = 'women'


class LiujoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-main-info .price::text'
    one_color = 'One Color'

    def parse(self, response):

        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['gender'] = self.gender
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        sku = deepcopy(self.product_pricing_common_new(response))
        sku['currency'] = 'EUR'
        sizes = clean(response.css('#configurable_swatch_liujo_size [name]::attr(title)'))

        for color_sel in response.css('#configurable_swatch_color [name]'):
            sku_id = clean(color_sel.css('::attr(id)'))[0]
            sku['color'] = clean(color_sel.css('::attr(name)'))[0]

            if sizes:
                for size in sizes:
                    sku['size'] = size
                    skus[sku_id+'-'+size] = deepcopy(sku)
            else:
                sku['size'] = self.one_size
                skus[sku_id] = deepcopy(sku)

        if skus:
            return skus

        for size_sel in response.css('#configurable_swatch_liujo_size [name]'):
            sku_id = clean(size_sel.css('::attr(id)'))[0]
            sku['color'] = self.one_color
            sku['size'] = clean(size_sel.css('::attr(title)'))[0]

            skus[sku_id] = deepcopy(sku)

        return skus

    def image_urls(self, response):
        return clean(response.css('.product-media-gallery img::attr(data-more-views)'))

    def product_id(self, response):
        return clean(response.css('.product-ids::text'))[0].replace('Item ', '')

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_description(self, response):
        return clean(response.css('.short-description-value ::text'))

    def product_care(self, response):
        return [x for x in clean(response.css('.details-value ::text')) if self.care_criteria_simplified(x)]


class LiujoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LiujoParseSpider()

    listing_css = [
        '.second-level [target="_self"]',
    ]

    pagination_css = '[rel="next"]::attr(href)'

    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='paging_request'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item')
    )

    def paging_request(self, response):
        for request in self.parse(response):
            yield request

        if response.css(self.pagination_css):
            yield Request(url=clean(response.css(self.pagination_css))[0], callback=self.paging_request)