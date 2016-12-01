import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean
from titlecase import titlecase


class Mixin(object):
    lang = 'fr'
    market = 'FR'
    retailer = 'jennyfer-fr'
    base_url = "http://www.jennyfer.com"
    allowed_domains = ['www.jennyfer.com']
    start_urls = ['http://www.jennyfer.com/']
    gender = 'women'


class JennyferParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    PRICE_X = '//div[@class="pdp-top"]//span[contains(@class, "price")]//text()'

    def parse(self, response):
        pid = self.product_id(response.url)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response, response)
        garment['merch_info'] = self.merch_info(response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):

        sku_common = self.product_pricing_common(response)

        colour = self.sku_colour(response)
        sku_common['colour'] = colour

        skus = {}
        size_variations = self.sku_sizes(response)
        for size_data in size_variations:
            sku = sku_common.copy()
            sku['size'] = size_data['size']
            sku['out_of_stock'] = size_data['out_of_stock']

            skus[colour + '_' + size_data['size']] = sku

        return skus

    def colour_requests(self, response):
        css = '.variation-color .emptyswatch a::attr(href)'
        colour_links = clean(response.css(css))

        return [Request(link, callback=self.parse_colour) for link in colour_links]

    def product_id(self, url):
        return re.findall('-(\d+).html', url)[0]

    def image_urls(self, response):
        css = '.product-image-container .product-primary-image a::attr(href)'
        return [image for image in clean(response.css(css))]

    def product_brand(self, category):
        return 'Jennyfer'

    def product_name(self, response):
        css = '#product-content .product-name::text'
        return titlecase(clean(response.css(css))[0])

    def product_category(self, response):
        css = '.breadcrumb a span::text'
        return clean(response.css(css)[1:])

    def product_description(self, response):
        css = '.pdpForm div[itemprop="description"]::text'
        return clean(response.css(css))

    def product_care(self, response):
        css = '.pdpForm .laundry-care span::attr(title), .pdpForm .material::text'
        return clean(response.css(css))

    def sku_sizes(self, response):
        sizes = []
        css = '.variation-size .emptyswatch div'
        size_options = response.css(css)

        for size in size_options:
            data = {}
            size_text = clean(size.xpath('text()'))[0]
            out_of_stock_text = clean(size.xpath('@class'))[0]

            data['size'] = self.one_size if size_text == 'TU' else size_text
            data['out_of_stock'] = True if 'unselected' in out_of_stock_text else False
            sizes.append(data)

        return sizes

    def sku_colour(self, response):
        xpath = '//div[contains(@class, "variation-color")]//a[child::img[@class="selected"]]//@title'
        return clean(response.xpath(xpath))[0]

    def merch_info(self, response):
        css = '.product-image-container .flag .tag::text'
        return clean(response.css(css))


class JennyferCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = JennyferParseSpider()

    allow_r = [
        '/vetements/',
        '/accessoires/',
        '/style-guide/'
    ]

    listings_css = [
        '.level-2 a',
        '.pagination .arrow-page'
    ]

    products_css = [
        '#search-result-items .product-wrapper > a'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listings_css, allow=allow_r)),
    )
