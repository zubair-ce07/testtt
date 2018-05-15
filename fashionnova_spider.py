import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import urlsplit, urljoin, url_query_parameter, add_or_replace_parameter
from math import ceil

from skuscraper.parsers.jsparser import JSParser
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'fashionnova'
    allowed_domains = [
        'fashionnova.com',
        'ultimate-dot-acp-magento.appspot.com'
    ]
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
        return clean(response.css('h1.title::text'))[0]

    def product_category(self, response):
        css = 'script:contains(ProductCategories)'
        categories = response.css(css).re_first(r"'ProductCategories': '\[(.*?)\]'")
        return json.loads('[' + categories.replace('\\\'', '\'') + ']')

    def image_urls(self, response):
        images = clean(response.css('.productImage::attr(href)'))
        return [response.urljoin(img) for img in images]

    def skus(self, response):
        skus = {}

        css = 'script:contains("var json_product")::text'
        raw_product = JSParser(clean(response.css(css))[0])['json_product']

        for raw_sku in raw_product['variants']:
            sku_id = raw_sku['id']
            sku = self.product_pricing_common(response)
            size = raw_sku['title']
            sku['size'] = self.one_size if size == 'OS' else size
            sku['colour'] = re.search('- (.*?) -', raw_sku['name']).group(1)

            if not raw_sku['available']:
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus


class FashionNovaCrawlSpider(BaseCrawlSpider):
    listings_css = '.main-menu > ul > li > div > a'
    listings_url = 'https://ultimate-dot-acp-magento.appspot.com/categories_navigation?q='
    page_size = 32

    deny_r = ['pages']

    rules = [Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse')]

    def parse(self, response):
        yield from super().parse(response)

        category_path = urlsplit(response.url).path
        link_for_uuid = clean(response.xpath('//script[contains(@src, "UUID")]/@src'))[0]
        uuid = url_query_parameter(link_for_uuid, 'UUID')

        url = add_or_replace_parameter(self.listings_url, 'UUID', uuid)
        url = add_or_replace_parameter(url, 'page_num', 1)
        listing_url = add_or_replace_parameter(url, 'category_url', category_path)

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)
        yield Request(url=listing_url, callback=self.parse_listings, meta=meta)

    def parse_listings(self, response):
        yield from self.product_requests(response)

        if url_query_parameter(response.url, 'page_num') != '1':
            return

        listing = json.loads(response.text)
        total_products = listing['total_results']
        total_pages = ceil(total_products / self.page_size)

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for page_index in range(2, total_pages + 1):
            pagination_url = add_or_replace_parameter(response.url, 'page_num', page_index)
            yield Request(url=pagination_url, callback=self.parse_listings, meta=meta.copy())

    def product_requests(self, response):
        listing = json.loads(response.text)
        requests = []

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for item in listing['items']:
            product_url = urljoin(self.start_urls[0], item['u'])
            request = Request(url=product_url, callback=self.parse_item, meta=meta.copy())
            requests.append(request)

        return requests


class FashionNovaUSParseSpider(MixinUS, FashionNovaParseSpider):
    name = MixinUS.retailer + '-parse'


class FashionNovaUSCrawlSpider(MixinUS, FashionNovaCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = FashionNovaUSParseSpider()
