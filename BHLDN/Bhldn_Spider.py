from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, clean
import re
import json


class Mixin:
    retailer = 'bhldn-us'
    allowed_domains = ['bhldn.com']
    start_urls = ['http://www.bhldn.com/']
    market = 'US'
    brand = 'bhldr'


class BhldnParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.price::text'

    def parse(self, response):

        if clean(response.css('.moredetails-link')):
            return

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id[0])
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.gender(garment['url'])
        if not garment['gender']:
            garment['industry'] = 'homeware'
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)
        return garment

    def merch_info(self, response):
        return clean(response.css('.product-form__unavailable p::text'))

    def product_id(self, response):
        return clean(response.css('meta[itemprop=sku]::attr(content)'))

    def product_name(self, response):
        return clean(response.css('h1[itemprop=name]::text'))

    def product_description(self, response):
        return [rd for rd in self.clean_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.clean_description(response) if self.care_criteria(rd)]

    def clean_description(self, response):
        description = self.raw_description(response)
        for entry in list(description):
            if any(re.match(regex, entry) for regex in [r'All gowns .*', r'We recommend .*', r'See fit guide .*']):
                description.remove(entry)
        return description

    def raw_description(self, response):
        return clean(response.css('div[itemprop=description] ::text'))

    def product_brand(self, response):
        description = self.raw_description(response)
        for entry in list(description):
            if re.match(r'By .*', entry):
                return entry
        return 'bhldn'

    def image_urls(self, response):
        return clean(response.css('.js-bigimage::attr(href)'))

    def color(self, response):

        if len(clean(response.css('vProduct-productOptionsFields-color-1 option'))) > 2:
            color_id = response.url.split('/')[-1]
        else:
            color_id = clean(response.css('option::attr(value)'))[0]

        color = json.loads(clean(response.css('option[value="'+color_id+'"]::attr(data-color)'))[0])
        return color['NAME'], color_id

    def skus(self, response):
        color, color_id = self.color(response)
        sizes = response.css('select[data-color*="'+color_id+'"] option')[1:]
        skus = {}

        for size in sizes:
            availability = json.loads(clean(size.css('option::attr(data-availability)'))[0])['STATUS']
            if availability == 'instock':
                availability = True
            else:
                availability = False
            size_sku = clean(size.css('option::attr(value)'))[0]
            saleprice = json.loads(clean(size.css('option::attr(data-saleprice)'))[0])['SALEPRICE']
            price = json.loads(clean(size.css('option::attr(data-price)'))[0])['PRICE']
            price = self.product_pricing_common_new('', money_strs=[saleprice+price])
            size = clean(size.css('option::text'))[0]
            sku = {'color': color, 'size': size, 'out_of_stock': availability}
            sku.update(price)
            skus[size_sku] = sku

        return skus

    def gender(self, url):
        if 'groom' in url:
            return 'men'
        elif 'girl' in url:
            return 'girl'
        elif not 'decor' in url:
            return 'women'
        return


class BhldnCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BhldnParseSpider()

    listings_css = [".nav-secondary a", ".next a"]
    product_css = ".primary a"

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))

