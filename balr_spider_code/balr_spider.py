import json

from w3lib.url import url_query_parameter, add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender
from skuscraper.utils.market_lang import get_spider_lang


class Mixin:
    retailer = 'balr'
    allowed_domains = ['balr.com']
    MERCH_INFO = [
        'disponibilidad limitada',
        'beperkt verkrijgbaar',
        'edition limitée',
        'begrenzte verfügbarkeit'
    ]


class MixinDE(Mixin):
    market = 'DE'
    retailer = Mixin.retailer + '-de'
    start_urls = ['https://www.balr.com/de']


class MixinNL(Mixin):
    market = 'NL'
    retailer = Mixin.retailer + '-nl'
    start_urls = ['https://www.balr.com/nl']


class MixinES(Mixin):
    market = 'ES'
    retailer = Mixin.retailer + '-es'
    start_urls = ['https://www.balr.com/es']


class MixinFR(Mixin):
    market = 'FR'
    retailer = Mixin.retailer + '-fr'
    start_urls = ['https://www.balr.com/fr']


class BalrParseSpider(BaseParseSpider):
    description_css = '.product-desc-short ::text'
    care_css = '.product-care-tab::text'
    price_css = '.price ::text'
    default_brand = 'Balr'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['merch_info'] = self.merch_info(response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        garment['skus'] = self.skus(response)

        return garment

    def skus(self, response):
        skus = {}
        oos_css = '.carousel-product-variant::attr(data-availability-message)'
        availability = response.css(oos_css).extract()
        common = self.product_pricing_common(response)
        raw_product = self.raw_product(response)
        common['colour'] = raw_product['variant']
        sizes = raw_product['dimension2'] or [self.one_size]

        for size, is_oos in zip(sizes, availability):
            sku = common.copy()
            sku['size'] = size.replace('Size ', '')
            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku

            if is_oos:
                sku['out_of_stock'] = True

        return skus

    def merch_info(self, response):
        soup = (' '.join(clean(response.css('.product-detail-column.arrow-up ::text')))).lower()
        return [m for m in self.MERCH_INFO if m in soup]

    def product_category(self, response):
        raw_product = self.raw_product(response)
        return raw_product['category'].split('/')

    def product_id(self, response):
        raw_product = self.raw_product(response)
        return raw_product.get('id')

    def raw_product(self, response):
        raw_product = response.xpath('//script/text()').re_first(r'push\((.*Product.*)\)')
        return json.loads(raw_product)['ecommerce']['detail']['products'][0]

    def image_urls(self, response):
        code = clean(response.css('.carousel-product-variant::attr(data-code)'))[0]
        css = f'.carousel-product-variant[data-code="{code}"] > img::attr(src)'
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = ' '.join(garment['category'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_name(self, response):
        return clean(response.css('h1::text'))[0]


class BalrCrawlSpider(BaseCrawlSpider):
    category_css = '.menu-level-2'
    pagination_url_t = 'https://www.balr.com/{lang}/shop-api{category}?max=16&page=1'

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback="parse_category"),
    )

    def parse_category(self, response):
        category = response.url.split('/shop')[-1]
        url = self.pagination_url_t.format(lang=get_spider_lang(self), category=category)
        yield response.follow(url=url, meta={'trail': self.add_trail(response)}, callback=self.parse_pagination)

    def parse_pagination(self, response):
        yield from self.product_requests(response)
        next_page = json.loads(response.text)['pager']['has_next_page']

        if not next_page:
            return

        page_count = int(url_query_parameter(response.url, 'page')) + 1
        url = add_or_replace_parameter(response.url, 'page', page_count)

        yield response.follow(url, meta={'trail': self.add_trail(response)}, callback=self.parse_pagination)

    def product_requests(self, response):
        product_urls = self.product_urls(response)
        meta = {'trail': self.add_trail(response)}
        requests = []

        for product_url in product_urls:
            requests.append(Request(response.urljoin(product_url), meta=meta.copy(), callback=self.parse_item))

        return requests

    def product_urls(self, response):
        raw_products = json.loads(response.body)['product_thumbnails']
        return [raw_product['uri'] for raw_product in raw_products]


class BalrDEParseSpider(BalrParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class BalrDECrawlSpider(BalrCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = BalrDEParseSpider()


class BalrNLParseSpider(BalrParseSpider, MixinNL):
    name = MixinNL.retailer + '-parse'


class BalrNLCrawlSpider(BalrCrawlSpider, MixinNL):
    name = MixinNL.retailer + '-crawl'
    parse_spider = BalrNLParseSpider()


class BalrESParseSpider(BalrParseSpider, MixinES):
    name = MixinES.retailer + '-parse'


class BalrESCrawlSpider(BalrCrawlSpider, MixinES):
    name = MixinES.retailer + '-crawl'
    parse_spider = BalrESParseSpider()


class BalrFRParseSpider(BalrParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class BalrFRCrawlSpider(BalrCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = BalrFRParseSpider()

