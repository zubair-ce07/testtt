import json

from scrapy.linkextractors import LinkExtractor
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
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.sizes_requests(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colors_requests(self, response):
        links = [response.url if 'color=&' in link else link
                 for link in clean(response.css('.selectableSwatch::attr(data-swatch-href)'))]
        return [Request(link, callback=self.parse_color, dont_filter=True) for link in links]

    def sizes_requests(self, response):
        links = clean(response.css('.pdp-size-qty-container a::attr(href)'))
        return [Request(link, callback=self.parse_size, dont_filter=True) for link in links]

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
        raw_data = clean(response.css('[id="secret_sauce_product_json"]::text'))
        soup = raw_data[0] if raw_data else ''
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_previous_prices(self, response):
        return clean(response.css('.pdp-original-price::text'))

    def is_available(self, response):
        return not response.css('.soldout-title')

    def skus(self, response):
        raw_product = self.raw_product(response)

        sku = self.product_pricing_common(response)
        sku['size'] = raw_product['dimension13'] or self.one_size
        sku['colour'] = raw_product['dimension19']
        if not self.is_available(response):
            sku['out_of_stock'] = True

        return {f"{sku['colour']}_{sku['size']}": sku}


class DvfUSParseSpider(MixinUS, DvfParseSpider):
    name = MixinUS.retailer + '-parse'


class DvfCrawlSpider(BaseCrawlSpider):
    listings_css = ['.category-menu__sub-menu-list-item']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),
    )

    def parse_category(self, response):
        products = clean(response.css('.grid-tile.item .product-info a::attr(href)'))
        for product in products:
            yield response.follow(product, self.parse_item,
            meta=self.get_meta_with_trail(response))

        next_page = clean(response.css('.infinite-scroll-placeholder::attr(data-grid-url)'))
        if next_page:
            yield response.follow(next_page[0], self.parse_category)


class DvfUSCrawlSpider(MixinUS, DvfCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = DvfUSParseSpider()
