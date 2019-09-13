import json

from scrapy.link import Link
from scrapy.selector import Selector
from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    retailer = 'sussan'
    default_brand = 'Sussan'
    gender = Gender.WOMEN.value


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    start_urls = ['https://www.sussan.com.au/']
    allowed_domains = ['www.sussan.com.au']


class ParseSpider(BaseParseSpider):
    raw_description_css = '.short-description.std ::text, .productAttributes ::text'
    price_css = '.product-main-info .price-box :not([class^="pdpPromoBadge"]) ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {
            'requests_queue': self.color_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = '.product-ids::text'
        return clean(response.css(css))[0].split('-')[0]

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumb a ::text'))[1:]

    def image_urls(self, response):
        return clean(response.css('.flexslider .slides li::attr(data-thumb)'))

    def color_requests(self, response):
        colours_css = '.colourSwatch option::attr(value)'
        colours = clean(response.css(colours_css))
        return [Request(colour, self.parse_colour) for colour in colours]

    def skus(self, response):
        skus = {}
        colour_css = '.colourSwatchWrapper option[selected="selected"]::text'
        common_sku = self.product_pricing_common(response)

        colour = clean(response.css(colour_css))
        if colour:
            common_sku["colour"] = colour[0]

        product_data = self.magento_product_data(response)
        if not product_data:
            common_sku['size'] = self.one_size
            sku_id = f'{common_sku["colour"]}_{common_sku["size"]}' if colour else common_sku['size']
            skus[sku_id] = common_sku
            return skus

        for raw_sku in self.magento_product_map(product_data).values():
            sku = common_sku.copy()
            size = raw_sku[0]['label']

            if 'Sold Out' in size:
                sku['out_of_stock'] = True

            sku['size'] = clean(size.split('-')[0])

            skus[f"{sku['colour']}_{sku['size']}" if colour else sku['size']] = sku
        return skus


class PaginationLE:
    PAGE_SIZE = 24

    def extract_links(self, response):
        product_count_css = '.numberOfResults::text'
        product_count = response.css(product_count_css).re_first("(\d+)")

        if not product_count:
            return []

        page_count = (int(product_count) // self.PAGE_SIZE) + 2

        return [Link(add_or_replace_parameters(response.url, {'ajax': 1, 'p': page}))
                for page in range(1, page_count)]


class CrawlSpider(BaseCrawlSpider):
    listings_css = ['[role="navigation"]']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(PaginationLE(), callback='product_requests'),
    )

    def product_requests(self, response):
        products_css = '.product-name a::attr(href)'

        product_sel = Selector(text=json.loads(response.text)['product_list'])
        meta = self.get_meta_with_trail(response)

        return [Request(product_url, callback=self.parse_item, meta=meta,)
                for product_url in clean(product_sel.css(products_css))]


class ParseSpiderAU(MixinAU, ParseSpider):
    name = MixinAU.retailer + '-parse'


class CrawlSpiderAU(MixinAU, CrawlSpider):
    name = MixinAU.retailer + '-crawl'
    parse_spider = ParseSpiderAU()
