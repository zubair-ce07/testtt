import json

from scrapy.link import Link
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor

from .base import clean
from .base import BaseParseSpider, BaseCrawlSpider
from skuscraper.parsers.genders import Gender


class Mixin:
    auto_proxy = True
    retailer = 'loro-piana'
    default_brand = 'Loro Piana'

    skus_url_t = '/api/pdp/product-variants?articleCode={}&colorCode={}'
    images_url_t = '/api/pdp/get-images?articleCode={}&colorCode={}'

    care_keywords = [
        '%',
        'iron',
        'clean',
        'wash'
    ]


class MixinUS(Mixin):
    market = 'US'
    retailer = Mixin.retailer + '-us'

    allowed_domains = ['us.loropiana.com']
    start_urls = ['https://us.loropiana.com/en']


class MixinUK(Mixin):
    market = 'UK'
    retailer = Mixin.retailer + '-uk'

    allowed_domains = ['uk.loropiana.com']
    start_urls = ['https://uk.loropiana.com/en']


class MixinIT(Mixin):
    market = 'IT'
    retailer = Mixin.retailer + '-it'

    allowed_domains = ['it.loropiana.com']
    start_urls = ['https://it.loropiana.com/it']

    care_keywords = [
        'lavare ',
        'stirare',
        'consiglia',
        '%',
    ]


class LoroPianaParseSpider(BaseParseSpider, Mixin):
    care_css = '#accordion_care .content::text'
    description_css = '.t-caption::text'
    raw_description_css = '.desktop-details p::text'

    one_sizes = ['NR']

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if not garment['industry']:
            garment['gender'] = self.gender_lookup(' '.join(garment['category'])) or Gender.ADULTS.value

        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.colour_requests(response, pid) + self.image_requests(response, pid),
        }

        return self.next_request_or_garment(garment)

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('.product-info .t-product-copy::text').re_first('(.*)\s/'))

    def product_name(self, response):
        return clean(response.css('.product-info h1::text').extract_first() or '').title()

    def product_price(self, response):
        return clean(response.css('.t-product-cta-price::text'))[0]

    def product_category(self, response):
        return clean(response.url.split('/')[5:-1])

    def product_colours(self, response):
        raw_colours = clean(response.css('#js-pdp-initial-variants::attr(value)'))[0]
        return json.loads(raw_colours)

    def care_criteria(self, text):
        return any(care_kw in text.lower() for care_kw in self.care_keywords)

    def skus(self, response):
        skus = {}

        sku_data = json.loads(response.text)[0]
        money_strs = [response.meta['price']]
        common_sku = self.product_pricing_common(None, money_strs=money_strs)
        common_sku['colour'] = sku_data['description']

        for sku_size in sku_data['sizes']:
            sku = common_sku.copy()

            sku['size'] = self.one_size if sku_size['code'] in self.one_sizes else sku_size['code']
            if sku_size['stock']['stockLevel'] == 0:
                sku['out_of_stock'] = True
            sku_id = sku_size['variantCode']

            skus[sku_id] = sku

        return skus

    def image_urls(self, response):
        raw_images = json.loads(response.text)
        return [im['url'] for formats in raw_images for im in formats['formats'] if im['format'] == 'ZOOM']

    def colour_requests(self, response, pid):
        colours = self.product_colours(response)
        meta = {'price': self.product_price(response)}
        return [response.follow(self.skus_url_t.format(pid, c['code']), callback=self.parse_colours,
                                meta=meta.copy()) for c in colours]

    def image_requests(self, response, pid):
        colours = self.product_colours(response)
        return [response.follow(self.images_url_t.format(pid, c['code']), callback=self.parse_images)
                for c in colours]


class PaginationLE(LinkExtractor):
    pagination_url_t = '/c/{}/results'

    def extract_links(self, response):

        if 'results' in response.url:
            pagination_data = json.loads(response.text)['pagination']
            current_page = pagination_data['currentPage']
            total_pages = pagination_data['numberOfPages']

            if current_page >= total_pages:
                return []

            url = add_or_replace_parameter(response.url, 'page', current_page+1)
            return [Link(url)]

        category_id = response.css('#js-category-vue-entry::attr(data-category-code)')
        pagination_data = response.css('#js-category-vue-entry::attr(data-pagination)')

        if category_id and pagination_data:
            total_pages = json.loads(clean(pagination_data)[0])['numberOfPages']

            if total_pages <= 1:
                return []

            url = response.urljoin(self.pagination_url_t.format(clean(category_id)[0]))
            url = add_or_replace_parameter(url, 'page', 1)
            return [Link(url)]

        return []


class ProductsLE(LinkExtractor):
    def extract_links(self, response):
        if 'results' not in response.url:
            return []

        raw_listings = json.loads(response.text)['results']
        return [Link(response.urljoin(raw_url['url'])) for raw_url in raw_listings]


class LoroPianaCrawlSpider(BaseCrawlSpider, Mixin):
    listings_css = '.safari_only'
    homeware_listings_css = '#submenu-HomeNavNode'
    products_css = ['.product-result', '.collection-section']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=homeware_listings_css), callback='parse_and_add_homeware'),
        Rule(PaginationLE(), callback='parse'),
        Rule(ProductsLE(), callback='parse_item'),
    )


class LoroPianaUSParseSpider(LoroPianaParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class LoroPianaUSCrawlSpider(LoroPianaCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = LoroPianaUSParseSpider()


class LoroPianaUKParseSpider(LoroPianaParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class LoroPianaUKCrawlSpider(LoroPianaCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = LoroPianaUKParseSpider()


class LoroPianaITParseSpider(LoroPianaParseSpider, MixinIT):
    name = MixinIT.retailer + '-parse'


class LoroPianaITCrawlSpider(LoroPianaCrawlSpider, MixinIT):
    name = MixinIT.retailer + '-crawl'
    parse_spider = LoroPianaITParseSpider()

