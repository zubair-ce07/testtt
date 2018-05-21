import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import url_query_parameter, url_query_cleaner, add_or_replace_parameter
from math import ceil

from skuscraper.parsers.jsparser import JSParser
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'fashionnova'
    allowed_domains = ['fashionnova.com']
    start_urls = ['https://www.fashionnova.com/']
    default_brand = 'Fashion Nova'
    gender = 'women'


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'


class FashionNovaParseSpider(BaseParseSpider):
    price_css = '.price span ::text'
    raw_description_css = 'div.description:not(.hide) li::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        self.boilerplate_minimal(garment, response, response.url)

        garment['merch_info'] = self.merch_info([garment['name']] + garment['description'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return [garment] + self.colour_requests(response)

    def colour_requests(self, response):
        urls = clean(response.css('.link-color-swatch::attr(href)'))
        meta = response.meta.copy()
        return [response.follow(url=url, callback=self.parse, meta=meta.copy()) for url in urls]

    def product_id(self, response):
        return clean(response.css('.product_id::text'))[0]

    def product_name(self, response):
        name = clean(response.css('h1.title::text'))[0]
        return name.split(' - ')[0]

    def product_category(self, response):
        css = 'script:contains(ProductCategories)'
        categories = response.css(css).re_first(r"'ProductCategories': '\[(.*?)\]'")
        return json.loads('[' + categories.replace('\\\'', '\'') + ']')

    def merch_info(self, description):
        merch_info = []

        for text in description:
            if 'limited edition' in text.lower():
                merch_info.append('Limited Edition')

        return merch_info

    def image_urls(self, response):
        images = clean(response.css('.productImage::attr(href)'))
        return [response.urljoin(img) for img in images]

    def skus(self, response):
        skus = {}

        css = 'script:contains("var json_product")::text'
        raw_product = JSParser(clean(response.css(css))[0])['json_product']
        base_sku = self.product_pricing_common(response)

        raw_colour = [tag for tag in raw_product['tags'] if 'Color-' in tag]
        raw_colour = raw_colour[0].strip('Color-') if raw_colour else ''
        base_colour = re.sub(r'(\w)([A-Z])', r"\1 \2", raw_colour)

        for raw_sku in raw_product['variants']:
            sku_id = raw_sku['id']
            sku = base_sku.copy()
            size = raw_sku['title']
            sku['size'] = self.one_size if size == 'OS' else size
            colour = re.search('- (.*?) -', raw_sku['name'])
            sku['colour'] = colour.group(1) if colour else base_colour

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus


class FashionNovaCrawlSpider(BaseCrawlSpider):
    listings_css = '.main-menu'
    products_css = '.product-item .info'

    page_size = 50

    deny_r = ['pages']

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner),
             callback='parse_item'),
    ]

    def parse(self, response):
        yield from super().parse(response)

        if url_query_parameter(response.url, 'page'):
            return

        total_products = response.css('.total-items::text').re_first('(\d+) styles') or '0'
        total_products = int(total_products)
        total_pages = ceil(total_products / self.page_size)

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for page_index in range(2, total_pages + 1):
            pagination_url = add_or_replace_parameter(response.url, 'page', page_index)
            request = Request(url=pagination_url, callback=self.parse, meta=meta.copy())
            yield request


class FashionNovaUSParseSpider(MixinUS, FashionNovaParseSpider):
    name = MixinUS.retailer + '-parse'


class FashionNovaUSCrawlSpider(MixinUS, FashionNovaCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = FashionNovaUSParseSpider()
