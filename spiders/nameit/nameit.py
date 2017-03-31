import json
from w3lib.url import add_or_replace_parameter, url_query_cleaner
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse, parse_qs
from scrapy.spiders import Rule
from scrapy import Request
from .base import BaseParseSpider, CurrencyParser, BaseCrawlSpider


class Mixin:
    retailer = 'nameit'
    allowed_domains = ['nameit.com']
    pfx = 'http://nameit.com/'


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    lang = 'de'
    start_urls = [Mixin.pfx + 'de/de/']
    gender_map = (
        ('a4dchen', 'girls'),
        ('junge', 'boys'),
        ('unisex', 'unisex-kids')
    )

class MixinNL(Mixin):
    retailer = Mixin.retailer + '-nl'
    market = 'NL'
    lang = 'nl'
    start_urls = [Mixin.pfx + 'nl/nl/']

    gender_map = (
        ('meisje', 'girls'),
        ('jongen', 'boys'),
        ('unisex', 'unisex-kids')
    )


class MixinBE(Mixin):
    retailer = Mixin.retailer + '-be'
    market = 'BE'
    lang = 'nl'
    start_urls = [Mixin.pfx + 'be/nl/']

    gender_map = (
        ('meisje', 'girls'),
        ('jongen', 'boys'),
        ('unisex', 'unisex-kids')
    )


class MixinCH(Mixin):
    retailer = Mixin.retailer + '-ch'
    market = 'CH'
    lang = 'de'
    start_urls = [Mixin.pfx + 'ch/de/']
    gender_map = (
        ('a4dchen', 'girls'),
        ('junge', 'boys'),
        ('unisex', 'unisex-kids')
    )


class NameitParseSpider(BaseParseSpider, Mixin):

    def parse(self, response):

        item = self.product(response)
        product = item[0]['ecommerce']['detail']['products'][0]
        pid = product['id']
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['name'] = product['name']
        garment['description'] = self.product_description(response)
        garment['brand'] = product['brand']
        garment['category'] = product['category']
        garment['care'] = self.product_care(response)
        garment['gender'] = self.product_gender(response)
        garment['merch_info'] = []
        response.meta['item'] = item
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)


    def product(self, response):
        xpath = "//script[contains(.,'dataLayer =')]/text()"
        product = response.xpath(xpath).extract_first().replace('dataLayer = ','')
        return json.loads(product[:-2])

    def product_description(self, response):
        return response.css('.pdp-description__text__short li::text').extract()

    def product_care(self, response):
        fabric = response.css('.pdp-description__text__value--fabric::text').extract()
        care = response.css('.pdp-description__list__item::text').extract()
        return fabric+care

    def image_urls(self, response):
        return response.css('.product-images__main__image img::attr(src)').extract()

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        parent_class = response.css('.js-swatch-item.swatch__item--selectable-colorpattern')
        urls = parent_class.css('a::attr(data-href)').extract()
        requests = []
        for url in urls:
            url = add_or_replace_parameter(url,'Quantity','1')
            url = add_or_replace_parameter(url, 'format', 'ajax')
            request = Request(url, callback=self.parse_colour, meta=response.meta.copy())
            requests.append(request)
        return requests

    def product_gender(self, response):
        return self.detect_gender(response.meta['trail'][0][1], self.gender_map)

    def common_sku(self, response):
        item = response.meta['item'][0]['ecommerce']
        prices = item['detail']['products'][0]
        sku = {}

        sku['price'] = CurrencyParser.prices(prices['salesPrice'])[0]
        prev_price = CurrencyParser.prices(prices['price'])
        if prev_price[0] != sku['price']:
            sku['previous_prices'] = prev_price
        sku['colour'] = response.css('.color-combination::text').extract_first()
        sku['currency'] = item['currencyCode']

        return sku

    def skus(self, response):
        skus = {}
        common_sku = self.common_sku(response)
        sizes = response.css('.swatch.size>li>a::text').extract()

        for size in sizes:
            sku = common_sku.copy()
            sku['out_of_stock'] = False
            sku['size'] = size.strip()
            sku_id = '{0}_{1}'.format(sku['colour'], sku['size'])
            skus[sku_id] = sku

        return skus


class NameitCrawlSpider(BaseCrawlSpider):

    products = ['.product-tile__name']
    listings = ['.category-navigation__group--level-2']

    rules = (

        Rule(LinkExtractor(restrict_css=products, process_value=url_query_cleaner),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings), callback='parse_gender')

    )

    def parse_gender(self, response):
        css = '.refine-filter__type-gender>ul>li>h5>a::attr(data-href)'
        genders = response.css(css).extract()

        for gender in genders:
            yield Request(gender, callback=self.parse_pagination)

    def parse_pagination(self, response):

        if not 'start' in response.url:
            next = 60
        else:
            params = urlparse(response.url).query
            next = int(parse_qs(params)['start'][0]) + 60

        next_page = response.css('.paging-controls__next::attr(data-href)').extract_first()
        trail = self.add_trail(response)
        yield Request(response.url, meta={'trail': trail}, dont_filter=True)

        if next_page:
            next_url = add_or_replace_parameter(next_page, "start", next)
            yield Request(next_url, callback=self.parse_pagination)


class NameitDEParseSpider(NameitParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class NameitDECrawlSpider(NameitCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = NameitDEParseSpider()


class NameitNLParseSpider(NameitParseSpider, MixinNL):
    name = MixinNL.retailer + '-parse'


class NameitNLCrawlSpider(NameitCrawlSpider, MixinNL):
    name = MixinNL.retailer + '-crawl'
    parse_spider = NameitNLParseSpider()


class NameitBEParseSpider(NameitParseSpider, MixinBE):
    name = MixinBE.retailer + '-parse'


class NameitBECrawlSpider(NameitCrawlSpider, MixinBE):
    name = MixinBE.retailer + '-crawl'
    parse_spider = NameitBEParseSpider()


class NameitCHParseSpider(NameitParseSpider, MixinCH):
    name = MixinCH.retailer + '-parse'


class NameitCHCrawlSpider(NameitCrawlSpider, MixinCH):
    name = MixinCH.retailer + '-crawl'
    parse_spider = NameitCHParseSpider()