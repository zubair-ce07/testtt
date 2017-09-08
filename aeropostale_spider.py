from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "aeropostale-us"
    market = 'US'
    allowed_domains = ['aeropostale.com']

    start_urls = [
        'http://www.aeropostale.com/textured-crew-tee/81431109.html']

    brands = [
        'AERO',
        'A87 NYC',
        'LIVE LOVE DREAM'
    ]


class AeropostaleParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = '.product-detail .product-price .price-msrp::text,' \
                '.product-detail .product-price .price-sale::text '

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)

        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = []

        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('span[itemprop="productID"] ::text'))[0]

    def raw_description(self, response):
        return clean(response.css('.tabs :not(:contains("Review"))::text'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_name(self, response):
        return response.css('.product-name ::text').extract_first()

    def product_category(self, response):
        return clean(response.css('a.breadcrumb-element ::text'))

    def product_brand(self, response):
        raw_brand = " ".join([self.product_name(response)] + self.product_category(response)).upper()

        for brand in self.brands:
            if brand in raw_brand:
                return brand
        return "AEROPOSTALE"

    def product_gender(self, garment):
        raw_gender = " ".join(garment['category']).lower()
        return "men" if "guys" in raw_gender else "women"

    def image_urls(self, response):
        return response.css('.product-primary-image  a::attr(href)').extract()

    def skus(self, response):
        sku = {'colour': response.css('.selected-value ::text').extract_first()}

        size = clean(response.css('.variation-select option[selected]::text'))
        sku['size'] = size[0] if size else self.one_size

        sku.update(self.product_pricing_common_new(response))
        if 'not available' in clean(response.css('span[itemprop="availability"]'))[0]:
            sku['out_of_stock'] = True

        return {sku['colour'] + "_" + sku['size']: sku}

    def size_requests(self, response):
        sizes = clean(response.css('.variation-select ::attr(value)'))
        return [Request(size, dont_filter=True, callback=self.parse_size) for size in sizes]

    def colour_requests(self, response):
        colours = clean(response.css('li[class="selectable"] ::attr(href)'))
        return [Request(colour, callback=self.parse_colour) for colour in colours]


def process_value(value):
    return value.split('?')[0]


class AeropostaleCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = AeropostaleParseSpider()

    products_css = '.search-result-items'

    listing_css = [
        '.menu-category',
        '.infinite-scroll-placeholder'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=['div', 'a'], attrs=['data-grid-url', 'href']),
             callback='parse'),

        Rule(LinkExtractor(restrict_css=products_css, process_value=process_value), callback='parse_item'),
    )
