import re
import json
from scrapy.http import Request
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean
from ..parsers.currencyparser import CurrencyParser


class Mixin:
    retailer = 'whitestuff'
    market = 'UK'
    allowed_domains = ['whitestuff.com']
    start_urls = ['https://www.whitestuff.com']
    gender_map = [
        ('womens', 'women'),
        ('mens', 'men'),
        ('boys', 'boys'),
        ('girls', 'girls'),
        ('kids', 'unisex-kids')
    ]


class WhiteStuffParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        request_url = clean(response.css('.product-form script::attr(src)'))[0]
        request = self.skus_request(request_url)
        garment['meta'] = {'requests_queue': request}
        return self.next_request_or_garment(garment)

    def skus_request(self, request_url):
        return [Request(request_url, self.parse_skus, dont_filter=True)]

    def parse_skus(self, response):
        garment = self.extract_skus(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[itemprop="sku"]::text'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        description = clean(response.css('.product-info__desc::text'))
        return description if description else []

    def product_category(self, response):
        return clean(response.css('.breadcrumb-list__item-link::text'))[1:]

    def product_care(self, response):
        return clean(response.css('.ish-ca-type::text, .ish-ca-value::text'))

    def product_gender(self, garment):
        soup = garment['category']
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        css = '.product-image__main img::attr(src)'
        return [url_query_cleaner(u) for u in clean(response.css(css))]

    def clean_json(self, json):
        return json.replace('//this is temporary until the feature is supported in the backoffice','')

    def extract_skus(self, response):
        garment = response.meta['garment']
        response_json = re.findall('({.*})', response.text, flags=re.DOTALL)
        response_json = self.clean_json(response_json[0])
        response_json = re.sub(r"(?<!\\)\\'", "'", response_json)
        response_json = json.loads(response_json)
        if response_json['productPrice'] == "N/A" or not response_json['inStock']:
            garment['out_of_stock'] = True
            return garment
        raw_skus = response_json['productVariations']
        for sku_key in raw_skus:
            sku = raw_skus[sku_key]
            if sku['salePrice'] == "N/A" or sku['listPrice'] == "N/A":
                return garment
            currency, price = CurrencyParser.currency_and_price(sku['salePrice'])
            _, previous_prices = CurrencyParser.currency_and_price(sku['listPrice'])
            sku_id = sku['productSKU']
            garment['skus'][sku_id] = {
                'colour': sku['colour'],
                'size': sku['size'],
                'currency': currency,
                'price': price,
                "previous_prices": [previous_prices],
                'out_of_stock': sku["inStock"]
            }
        return garment


class WhiteStuffCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WhiteStuffParseSpider()
    listing_css = ['#js-header-navbar']
    products_css = ['.seoworkaround']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
