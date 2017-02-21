import json

from scrapy.http.request import Request
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders.crawl import Rule
from w3lib.url import add_or_replace_parameter

from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser


class Mixin:
    retailer = 'hunkemoller'
    gender = 'women'


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    lang = 'de'
    allowed_domains = ['hunkemoller.de']
    start_urls = ['https://www.hunkemoller.de/de_de/']


class MixinNL:
    retailer = Mixin.retailer + '-nl'
    market = 'NL'
    lang = 'nl'
    allowed_domains = ['hunkemoller.nl']
    start_urls = ['https://www.hunkemoller.nl/nl_nl/']


class MixinAT:
    retailer = Mixin.retailer + '-at'
    market = 'AT'
    lang = 'de'
    allowed_domains = ['hunkemoller.at']
    start_urls = ['https://www.hunkemoller.at/at_at/']


class ParseSpider(BaseParseSpider):

    brands = [
        'Doutzen Sport',
        'Fifty Shades Darker',
        'HKMX',
        'HKM',
    ]

    def parse(self, response):
        product = self.raw_product(response)
        garment = self.new_unique_garment(product['id'])
        if garment is None:
            return
        self.boilerplate_minimal(garment, response)
        garment['brand'] = self.product_brand(product)
        garment['name'] = product['name']
        garment['category'] = self.product_category(response)
        garment['description'] = self.product_description(product)
        garment['care'] = self.product_care(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        if not garment['skus']:
            garment['out_of_stock'] = True
            garment.update(self.product_pricing_common(response))
        return garment

    def product_brand(self, product):
        raw_description = self.product_description(product) + [product['name']]
        raw_description = ' '.join(raw_description).title()
        for brand in self.brands:
            if brand in raw_description:
                return brand

        return 'Hunkemoller'

    def raw_product(self, response):
        product_re = 'product.productInfo\s*=\s*(\{.*\})'
        return json.loads(response.css('script.kega-ddl-script').re_first(product_re))

    def product_description(self, product):
        return self.text_from_html(product['description'])

    def product_care(self, response):
        return clean(response.css('.product-info ul.washing-tips *::text'))

    def product_category(self, response):
        page_info_re = 'page.pageInfo\s*=\s*(\{.*\})'
        page_info = json.loads(response.css('script.kega-ddl-script').re_first(page_info_re))
        return page_info['breadCrumbs'][1:-1]

    def product_currency(self, response):
        currency_re = "digitalData.product.currency\s*=\s*'(.*)';"
        return response.css('script.kega-ddl-script').re_first(currency_re)

    def product_pricing_common(self, response):
        pricing = {}
        pricing_re = 'Product.OptionsPrice\((\{.*\})\);'
        script_css = 'script:contains(optionsPrice)'
        price_info = json.loads(response.css(script_css).re_first(pricing_re))
        pricing['currency'] = self.product_currency(response)
        price = price_info['productPrice']
        pricing['price'] = CurrencyParser.float_conversion(price)
        if price_info.get('productOldPrice'):
            old_price = price_info['productOldPrice']
            if old_price != price:
                pricing['previous_prices'] = [CurrencyParser.float_conversion(old_price)]
        return pricing

    def skus(self, response):
        skus = {}
        size_css = '#product_addtocart_form option[data-additional]'
        size_s = response.css(size_css)
        sku_common = self.product_pricing_common(response)
        for s_s in size_s:
            sku = sku_common.copy()
            _, sku_info = json.loads(clean(s_s.css('::attr(data-additional)'))[0]).popitem()
            if not sku_info['is_in_stock']:
                sku['out_of_stock'] = True
            sku_id = sku_info['product_sku']
            skus[sku_id] = sku
        return skus

    def image_urls(self, response):
        return [json.loads(clean(a.css('::attr(rel)'))[0])['largeimage'] for a in response.css('#thumblist a')]


def make_rules(locale_filter=()):
    listing_css = ['.nav', '.current-category']
    products_css = ['.product-zoom']

    rules = (Rule(LinkExtractor(restrict_css=listing_css, allow=locale_filter), callback='parse_listing'),
             Rule(LinkExtractor(restrict_css=products_css, allow=locale_filter), callback='parse_item'))

    return rules


class CrawlSpider(BaseCrawlSpider):

    def parse_listing(self, response):
        for request in self.parse(response):
            yield request

        pages_s = response.css('.pages .last::text')
        max_pages = int(clean(pages_s)[0]) if pages_s else 0
        for p in range(1, max_pages+1):
            url = add_or_replace_parameter(response.url, 'p', str(p))
            meta = {'trail': self.add_trail(response)}
            yield Request(url=url, meta=meta, callback=self.parse_listing)


class ParseSpiderDE(MixinDE, ParseSpider):
    name = MixinDE.retailer + '-parse'


class CrawlSpiderDE(MixinDE, CrawlSpider):
    name = MixinDE.retailer + '-crawl'
    parse_spider = ParseSpiderDE()
    rules = make_rules('/de_de')


class ParseSpiderNL(MixinNL, ParseSpider):
    name = MixinNL.retailer + '-parse'


class CrawlSpiderNL(MixinNL, CrawlSpider):
    name = MixinNL.retailer + '-crawl'
    parse_spider = ParseSpiderNL()
    rules = make_rules('/nl_nl')


class ParseSpiderAT(MixinAT, ParseSpider):
    name = MixinAT.retailer + '-parse'


class CrawlSpiderAT(MixinAT, CrawlSpider):
    name = MixinAT.retailer + '-crawl'
    parse_spider = ParseSpiderAT()
    rules = make_rules('/at_at')

