import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'loropiana'
    default_brand = 'Loro Piana'
    allowed_domains = ['loropiana.com']

    image_url_t = "https://{}.loropiana.com/en/api/pdp/get-images?articleCode={}&colorCode={}"
    variant_url_t = "https://{}.loropiana.com/en/api/pdp/product-variants?articleCode={}&colorCode={}"


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls = ['https://us.loropiana.com/en/']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['https://uk.loropiana.com/en/']


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    market = 'IT'
    start_urls = ['https://it.loropiana.com/it/']


class LoroPianaParseSpider(BaseParseSpider):
    one_sizes = [
        'NR'
    ]

    price_css = '.t-product-cta-price ::text'
    raw_description_css = '.desktop-details .t-product-copy ::text'
    description_css = '.product-info .t-caption ::text'
    care_css = '#accordion_care .content ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['gender'] = self.product_gender(response)

        requests_queue = self.request_variants(response) + self.request_image_urls(response)
        garment['meta'] = {'requests_queue': requests_queue}

        return self.next_request_or_garment(garment)

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        variant = json.loads(response.text)[0]
        colour = variant['description']
        sku = response.meta['pricing_common']
        sku['colour'] = colour

        for sizes in variant['sizes']:
            size = sizes['code']
            sku['size'] = self.one_size if size.lower() in self.one_sizes else size

            if sizes['stock']['stockLevelStatus']['code'] == 'outOfStock':
                sku['out_of_stock'] = True

            skus[f"{colour}_{size}"] = sku

        return skus

    def image_urls(self, response):
        image_urls = []
        for raw_image in json.loads(response.text):
            for image in raw_image['formats']:

                if image['format'] == 'ZOOM':
                    image_urls.append(image['url'])

        return image_urls

    def product_id(self, response):
        return clean(response.css('::attr("data-base-product-code")'))[0]

    def product_gender(self, response):
        trail = [url for _, url in response.meta.get('trail') or []]
        soup = [response.url] + self.product_category(response) + trail

        return self.gender_lookup(soupify(soup)) or Gender.ADULTS.value

    def product_category(self, response):
        css = '.t-product-breadcrumps ::text'
        return [c.replace('>', '') for c in clean(response.css(css))]

    def detect_colour_codes(self, response):
        css = '#js-pdp-initial-variants ::attr(value)'
        raw_variants = clean(response.css(css))[0]

        return [variant['code'] for variant in json.loads(raw_variants)]

    def request_image_urls(self, response):
        product_id = self.product_id(response)
        colour_requests = []

        for colour_code in self.detect_colour_codes(response):
            url = self.image_url_t.format(self.market.lower(), product_id, colour_code)
            colour_requests.append(Request(url, callback=self.parse_image_urls))

        return colour_requests

    def request_variants(self, response):
        product_id = self.product_id(response)
        meta = {'pricing_common': self.product_pricing_common(response=response)}
        variant_requests = []

        for colour_code in self.detect_colour_codes(response):
            url = self.variant_url_t.format(self.market.lower(), product_id, colour_code)
            variant_requests.append(Request(url, meta=meta, callback=self.parse_skus))

        return variant_requests

    def product_name(self, response):
        return clean(response.css('.product-info .t-h2 ::text'))[0]


class LoroPianaCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.safari_only'
    ]

    products_css = [
        '.product-result'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    ]


class LoroPianaUSParseSpider(MixinUS, LoroPianaParseSpider):
    name = MixinUS.retailer + '-parse'


class LoroPianaUSCrawlSpider(MixinUS, LoroPianaCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = LoroPianaUSParseSpider()


class LoroPianaUKParseSpider(MixinUK, LoroPianaParseSpider):
    name = MixinUK.retailer + '-parse'


class LoroPianaUKCrawlSpider(MixinUK, LoroPianaCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = LoroPianaUKParseSpider()


class LoroPianaITParseSpider(MixinIT, LoroPianaParseSpider):
    name = MixinIT.retailer + '-parse'


class LoroPianaITCrawlSpider(MixinIT, LoroPianaCrawlSpider):
    name = MixinIT.retailer + '-crawl'
    parse_spider = LoroPianaITParseSpider()
