import json

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.spiders import Rule, Request

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify

class Mixin:
    retailer = 'dvf'
    default_brand = "DvF"


class MixinUS(Mixin):
    allowed_domains = ["dvf.com"]
    retailer = Mixin.retailer + "-us"
    market = 'US'
    retailer_currency = 'USD'
    start_urls = ['https://www.dvf.com/']


class DvfParseSpider(BaseParseSpider):
    description_css = '.desktopDesc::text, .desktopDesc p::text'
    care_css = '.product-module.fabric::text, .product-module.fabric p::text'
    price_css = '.product-overview-price'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []
        garment['skus'] = {}

        garment['meta'] = {'requests_queue': self.colors_requests(response)}
        response.meta['garment'] = garment
        return self.parse_color(response)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colors_requests(self, response):
        links = [link for link in clean(response.css('.selectableSwatch::attr(data-swatch-href)'))
                 if not 'color=&' in link]
        return [Request(link, callback=self.parse_color) for link in links]

    def raw_product(self, response):
        return json.loads(clean(response.css('[id="product-gtm-data"]::attr(data-gtmdata)'))[0])

    def product_name(self, response):
        return clean(response.css('.product-overview-title::text'))[0]

    def product_id(self, response):
        return self.raw_product(response)['id']

    def product_brand(self, response):
        return self.raw_product(response)['brand']

    def image_urls(self, response):
        return clean(response.css(".js-vertical-slider-inner-wrapper img::attr(src)"))

    def product_category(self, response):
        return [self.raw_product(response)['category']]

    def product_gender(self, response):
        soup = soupify(clean(response.css('[id="secret_sauce_product_json"]::text')))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response):
        raw_product = self.raw_product(response)
        skus = {}

        sizes = clean(response.css('.pdp-size-qty-container .sizeText::text'))
        available_sizes = clean(response.css('.pdp-size-qty-container .available .sizeText::text'))
        for size in sizes:
            sku = self.product_pricing_common(response)
            sku['size'] = size
            sku['colour'] = raw_product['dimension19']
            if not size in available_sizes:
                sku['out_of_stock'] = True
            skus[f"{sku['colour']}_{sku['size']}"] = sku

        return skus


class DvfUSParseSpider(MixinUS, DvfParseSpider):
    name = MixinUS.retailer + '-parse'


class PaginationLE():

    def extract_links(self, response):
        next_page = clean(response.css('.infinite-scroll-placeholder::attr(data-grid-url)'))
        return next_page and [Link(next_page[0])]


class DvfCrawlSpider(BaseCrawlSpider):
    listings_css = ['.category-menu__sub-menu-list-item']
    products_css = ['.grid-tile.item .product-info a']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(PaginationLE(), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class DvfUSCrawlSpider(MixinUS, DvfCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = DvfUSParseSpider()

