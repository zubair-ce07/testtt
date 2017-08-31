from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "figleaves-uk"
    market = 'UK'
    allowed_domains = ['figleaves.com']
    start_urls = ['http://www.figleaves.com/uk/']


class FigLeavesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = '.product-detail .product-price ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.size_requests(response) + self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def product_gender(self, garment):
        if "Mens" in garment['category']:
            return "men"
        return "women"

    def raw_description(self, response):
        return clean(response.css('ul.product-details-list ::text'))[1:]

    def product_id(self, response):
        return self.raw_description(response)[-1]

    def product_description(self, response):
        raw_description = self.raw_description(response)
        raw_description.pop()
        return [rd for rd in raw_description if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_name(self, response):
        return response.css('.product-name ::text').extract_first()

    def product_brand(self, response):
        return response.css('.product-brand ::text').extract_first()

    def product_category(self, response):
        return clean(response.css('ul.breadcrumb a ::text'))

    def image_urls(self, response):
        return response.css('a.product-image::attr(href)').extract()

    def skus(self, response):
        skus = {}
        sku = {'colour': response.css('.selected-value ::text').extract_first()}
        sku['size'] = \
            clean(response.css('.product-content-bottom  .variation-select option[selected][data-lgimg]::text'))[0]
        skus[sku['colour'] + "_" + sku['size']] = sku
        return skus

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        for sku in garment['skus'].values():
            if sku['size'] in response.url:
                sku.update(self.product_pricing_common_new(response))
                if 'Out' in clean(response.css('.product-content-bottom .availability-msg ::text')):
                    sku['out_of_stock'] = True
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        sizes = clean(response.css('.product-content-bottom  .variation-select ::attr(value)'))
        return [Request(size, dont_filter=True, callback=self.parse_size) for size in sizes]

    def colour_requests(self, response):
        colours = clean(response.css('.product-content-bottom a[class="swatchanchor selectable"]::attr(href)'))
        return [Request(colour, dont_filter=True, callback=self.parse_colour) for colour in colours]


class FigLeavesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = FigLeavesParseSpider()

    pagination_css = [
        '.infinite-scroll-button',
        '.infinite-scroll-placeholder'
    ]

    products_css = '.search-result-items'

    deny = [
        '/gifts-and-accessories',
        '/my-perfect-fit'
    ]

    listing_css = [
        '.header-nav-strip',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=pagination_css, tags=['div', 'button'], attrs=['data-grid-url']),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
