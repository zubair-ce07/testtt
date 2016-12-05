import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, CurrencyParser, clean


class Mixin(object):
    lang = 'fr'
    market = 'FR'
    currency = 'EUR'
    retailer = 'jules-fr'
    base_url = "http://www.jules.com"
    allowed_domains = ['www.jules.com']
    start_urls = ['http://www.jules.com/fr/index']
    gender = 'men'


class JulesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    PRICE_X = '//div[@id="product-content"]//span[@itemprop="price"]//text()'

    def parse(self, response):
        pid = self.product_id(response.url)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response, response)
        garment['merch_info'] = self.merch_info(response)

        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        sku_common = self.product_pricing_common(response)
        sku_common['currency'] = clean(response.css('meta[itemprop="priceCurrency"]::attr(content)')[0])

        s_c = clean(response.css('.swatches-color .selected span::text'))
        if s_c:
            sku_common['colour'] = colour = s_c[0]

        skus = {}
        css = '.attribute-size li'
        sizes_s = response.css(css)
        for s_s in sizes_s:
            sku = sku_common.copy()
            size = clean(s_s.css('a::text, span::attr(title)'))[0]
            sku['size'] = size = self.one_size if size == 'T.U.' else size

            if s_s.css(".disabled"):
                sku['out_of_stock'] = True
            if s_c:
                skus[colour + '_' + size] = sku
            else:
                skus[size] = sku

        return skus

    def colour_requests(self, response):
        css = '.swatches-color li:not(.selected) a::attr(href)'
        colour_links = clean(response.css(css))

        return [Request(link, callback=self.parse_colour) for link in colour_links]

    def product_id(self, url):
        return re.findall('-(\d+).html', url)[0]

    def image_urls(self, response):
        css = '.product-image-link::attr(href)'
        return clean(response.css(css))

    def product_brand(self, category):
        return 'Jules, The Gentle Factory'

    def product_name(self, response):
        css = '.product-name .name::text'
        return re.sub(' La Gentle Factory$', '', clean(response.css(css))[0])

    def product_category(self, response):
        css = '.breadcrumb a span::text'
        return clean(response.css(css)[1:])

    def product_description(self, response):
        css = '.product-desc-long::text'
        return clean(response.css(css))

    def product_care(self, response):
        css = '#compositionandupkeep span::text'
        return clean(response.css(css)) + [c for c in self.product_description(response) if '%' in c]

    def merch_info(self, response):
        mi = clean(response.css('.product-flags img::attr(src)'))
        if mi and mi[0].endswith('124378.png'):
            return '-30% SUR LE 2EME ARTICLE* / -50% SUR LE 3EME ARTICLE*'


class JulesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = JulesParseSpider()

    allow_r = [
        '/hauts/',
        '/bas/',
        '/accessoires/',
        '/accessoires-5/',
        '/accessoires-6/',
    ]

    listings_css = [
        '.ul-level-2',
        'div.pagination li a'
    ]

    products_css = [
        '.product-image .thumb-link'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css, allow=allow_r), callback='parse'),
    )
