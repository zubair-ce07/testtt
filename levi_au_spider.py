import json
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter, url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'levi'


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    start_urls = ['https://www.levis.com.au/']
    allowed_domains = ['www.levis.com.au']


class MixinIN(Mixin):
    retailer = Mixin.retailer + '-in'
    market = 'IN'
    start_urls = ['https://www.levi.in']
    allowed_domains = ['www.levi.in']


class MixinKR(Mixin):
    retailer = Mixin.retailer + '-kr'
    market = 'KR'
    start_urls = ['https://www.levi.co.kr/home']
    allowed_domains = ['www.levi.co.kr']


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    start_urls = ['https://www.levi.jp/']
    allowed_domains = ['www.levi.jp']


class ParseSpider(BaseParseSpider):

    price_css = '.product-price :not(.promo-discount) ::text'
    description_css = '.product-details .tab-content ::text, .fit-and-size .tab-content ::text'
    care_css = '.product-material .tab-content ::text'

    def parse(self, response):

        if response.css('#product-set-list'):
            return

        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment,response)
        garment['gender'] = self.gender_lookup(response.url) or Gender.ADULTS.value
        garment['image_urls'] = []
        garment['skus'] = {}

        colour_requests = self.colour_requests(response)
        if not colour_requests:
            garment['image_urls'] += self.image_urls(response)
            garment['skus'].update(self.skus(response))
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        css = '.color li .swatchanchor::attr(href)'
        return [Request(url, dont_filter=True, callback=self.parse_colour) for url in clean(response.css(css))]

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        size_variant_requests = self.variant_request(response)

        if size_variant_requests:
            garment['meta']['requests_queue'] += size_variant_requests

        else:
            garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def variant_request(self, response):
        css = '.size li:not(.selected) .swatchanchor::attr(href)'
        return [Request(add_or_replace_parameter(url.replace('amp;', ''), 'format', 'ajax'),
                        dont_filter=True, callback=self.parse_variant) for url in clean(response.css(css))]

    def parse_variant(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('.product-number ::attr(data-masterid)'))[0]

    def product_name(self, response):
        return (' '.join(clean(response.css('h1.product-name::text, h2.product-name ::text')))).strip()

    def product_brand(self, response):
        return 'Levi'

    def image_urls(self, response):
        image_urls = clean(response.css('.product-thumbnails .productthumbnail::attr(data-lgimg)'))
        return [response.urljoin(json.loads(url)['zoomImg']) for url in image_urls]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = colour = clean(response.css('.color .selected-value::text'))[0]

        oos_sizes = clean(response.css('.size-waist-variation .unselectable ::text'))
        variant = clean(response.css('.size .selected ::text'))

        for size in clean(response.css('.size-waist-variation .swatchanchor ::text')):
            sku = common_sku.copy()

            if variant:
                size = f'{variant[0]}_{size}'

            sku['size'] = size = self.one_size if size in ['OS'] else size

            if size in oos_sizes:
                sku['out_of_stock'] = True

            skus[f'{colour}_{size}'] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.level-2',
    ]

    products_css = '.product-tile'

    deny_r = ['/discover', '/stories', '/fitchart']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner), callback='parse_item')
    )

    def parse_pagination(self, response):

        meta = {'trail': self.add_trail(response)}

        page_size = 12
        total_items = clean(response.css('.results-hits .style-count::text'))[0]
        total_items = int(re.findall('\d+', total_items)[0])

        url = add_or_replace_parameter(response.url, 'sz', page_size)
        url = add_or_replace_parameter(url, 'format', 'page-element')

        for start in range(0, total_items, page_size):
            url = add_or_replace_parameter(url, 'start', start)
            yield Request(response.urljoin(url), meta=meta.copy(), callback=self.parse)


class AUParseSpider(MixinAU, ParseSpider):
    name = MixinAU.retailer + '-parse'


class AUCrawlSpider(MixinAU, CrawlSpider):
    name = MixinAU.retailer + '-crawl'
    parse_spider = AUParseSpider()


class JPParseSpider(MixinJP, ParseSpider):
    name = MixinJP.retailer + '-parse'


class JPCrawlSpider(MixinJP, CrawlSpider):
    name = MixinJP.retailer + '-crawl'
    parse_spider = JPParseSpider()


class KRParseSpider(MixinKR, ParseSpider):
    name = MixinKR.retailer + '-parse'


class KRCrawlSpider(MixinKR, CrawlSpider):
    name = MixinKR.retailer + '-crawl'
    parse_spider = KRParseSpider()


class INParseSpider(MixinIN, ParseSpider):
    name = MixinIN.retailer + '-parse'


class INCrawlSpider(MixinIN, CrawlSpider):
    name = MixinIN.retailer + '-crawl'
    parse_spider = INParseSpider()

