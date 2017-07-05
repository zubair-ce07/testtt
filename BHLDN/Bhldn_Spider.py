import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'bhldn-us'
    allowed_domains = ['bhldn.com']
    start_urls = ['http://www.bhldn.com/']
    market = 'US'
    brand = 'bhldn'
    unwanted_description_re = [re.compile(r'All gowns .*'), re.compile(r'We recommend .*'),
                               re.compile(r'See fit guide .*')]
    gender_map = {'groom': 'men', 'girl': 'girl'}
    industry_map = {'decor': 'homeware'}


class BhldnParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.price::text'

    def parse(self, response):
        sku_id = self.product_id(response)

        if response.css('.moredetails-link').extract():
            return
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['industry'] = 'homeware' if self.is_industry(garment['url_original']) else None
        garment['gender'] = self.gender(garment['url_original']) if not garment['industry'] else None
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)

        return garment

    def is_industry(self, url):

        for industry_string, industry in self.industry_map.items():

            if industry_string in url:
                return True

        return False

    def merch_info(self, response):
        return clean(response.css('.product-form__unavailable p::text'))

    def product_id(self, response):
        return clean(response.css('meta[itemprop=sku]::attr(content)'))[0]

    def product_name(self, response):
        return clean(response.css('h1[itemprop=name]::text'))[0]

    def product_description(self, response):
        return [rd for rd in self.clean_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.clean_description(response) if self.care_criteria(rd)]

    def clean_description(self, response):
        description = self.raw_description(response)
        raw_description = []

        for rd in description:

            if not any(re.match(regex, rd) for regex in self.unwanted_description_re):
                raw_description.append(rd)

        return raw_description

    def raw_description(self, response):
        return clean(response.css('div[itemprop=description] ::text'))

    def product_brand(self, response):
        description = self.raw_description(response)

        for entry in description:

            if re.match(re.compile(r'By .*'), entry):
                return entry

        return 'bhldn'

    def image_urls(self, response):
        return clean(response.css('option[selected]::attr(value)'))

    def color(self, response):
        color_id = clean(response.css('option::attr(value)'))[0]
        color = json.loads(clean(response.css('option[value="'+color_id+'"]::attr(data-color)'))[0])

        return color['NAME'], color_id

    def skus(self, response):
        color, color_id = self.color(response)
        raw_skus = response.css('select[data-color*="'+color_id+'"] option')[1:]
        skus = {}

        for raw_sku in raw_skus:
            availability = self.sku_availability(raw_sku)
            sku_id = clean(raw_sku.css('option::attr(value)'))[0]
            pricing = self.product_price(raw_sku)
            size = clean(raw_sku.css('option::text'))[0]
            sku = {'colour': color, 'size': size}

            if not availability:
                sku['out_of_stock'] = availability
            sku.update(pricing)
            skus[sku_id] = sku

        return skus

    def product_price(self, raw_sku):
        saleprice = json.loads(clean(raw_sku.css('option::attr(data-saleprice)'))[0])['SALEPRICE']
        price = json.loads(clean(raw_sku.css('option::attr(data-price)'))[0])['PRICE']

        return self.product_pricing_common_new('', money_strs=[saleprice, price])

    def sku_availability(self, raw_sku):
        css = 'option::attr(data-availability)'
        availability = json.loads(clean(raw_sku.css(css))[0])

        return availability['STATUS'] == 'instock'

    def gender(self, url):

        for gender_string, gender in self.gender_map.items():

            if gender_string in url:
                return gender

        return 'women'


class BhldnCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BhldnParseSpider()

    listings_css = [".nav-secondary", ".next"]
    product_css = ".primary"

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))

