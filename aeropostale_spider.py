from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "aeropostale-us"
    market = 'US'
    allowed_domains = ['aeropostale.com']

    start_urls = [
        'http://www.aeropostale.com']

    brands = [
        'AERO',
        'A87 NYC',
        'LIVE LOVE DREAM'
    ]


class AeropostaleParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = '.product-detail .product-price ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)

        garment['brand'] = self.product_brand(response)
        garment['image_urls'] = self.image_urls(response)

        garment['skus'] = self.skus(response)
        colour_urls, colour_requests = self.colour_requests(response)
        garment['meta'] = {'requests_queue': self.size_requests(response) + colour_requests}

        garment['meta']['colour_urls'] = colour_urls
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('span[itemprop="productID"] ::text'))[0]

    def raw_description(self, response):
        return clean(response.css('.product-info ::text'))

    def product_description(self, response):
        return self.clean_description([rd for rd in self.raw_description(response) if not self.care_criteria(rd)])

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_name(self, response):
        return response.css('.product-name ::text').extract_first()

    def product_category(self, response):
        return clean(response.css('a.breadcrumb-element ::text'))

    def product_brand(self, response):
        raw_brand = "".join([self.product_name(response)] + self.product_category(response)).upper()

        for brand in self.brands:
            if brand in raw_brand:
                return brand
        return "AEROPOSTALE"

    def clean_description(self, description):
        index = None
        for line in description:
            if "Review" in line:
                index = description.index(line)

        return description[:index - 1]

    def product_gender(self, garment):
        gender = "women"
        for raw_gender in garment['category']:
            if "Guys" in raw_gender:
                gender = "men"
        return gender

    def image_urls(self, response):
        return response.css('.product-primary-image  a::attr(href)').extract()

    def skus(self, response):
        skus = {}
        sku = {'colour': response.css('.selected-value ::text').extract_first()}
        size = clean(response.css('.variation-select option[selected]::text'))
        if size:
            sku['size'] = size[0]
        else:
            sku['size'] = self.one_size

        sku.update(self.product_pricing_common_new(response, post_process=self.post_process))
        if 'not' in clean(response.css('span[itemprop="availability"]'))[0]:
            sku['out_of_stock'] = True

        skus[sku['colour'] + "_" + sku['size']] = sku
        return skus

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        for colour in clean(response.css('li[class="selectable"] ::attr(href)')):
            if colour not in garment['meta']['colour_urls']:
                garment['meta']['colour_urls'].append(colour)
                garment['meta']['requests_queue'].append(
                    Request(colour, dont_filter=True, callback=self.parse_colour))

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        sizes = clean(response.css('.variation-select ::attr(value)'))
        return [Request(size, dont_filter=True, callback=self.parse_size) for size in sizes]

    def colour_requests(self, response):
        colours = clean(response.css('li[class="selectable"] ::attr(href)'))
        return colours, [Request(colour, callback=self.parse_colour) for colour in colours]

    def post_process(self, money_strs):
        return money_strs[1:]


class AeropostaleCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = AeropostaleParseSpider()

    products_css = '.search-result-items'

    listing_css = [
        '.menu-category',
        '.infinite-scroll-placeholder'
    ]

    tags = ['div', 'a']

    attributes = ['data-grid-url', 'href']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=tags, attrs=attributes),
             callback='parse'),

        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
