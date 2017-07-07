import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'bhldn-us'
    allowed_domains = ['bhldn.com']
    start_urls = ['http://www.bhldn.com/bridal-party-flower-girl-dresses/?cm_sp=LEFTNAV-_-SUB_CATEGORY-_-BRIDALPARTY_FLOWERGIRLDRESSES',
                  'http://www.bhldn.com/bridal-party-groom-groomsmen/?cm_sp=LEFTNAV-_-SUB_CATEGORY-_-BRIDALPARTY_GROOM',
                  # 'http://www.bhldn.com/'
                  ]
    market = 'US'
    brand = 'bhldn'
    unwanted_description_re = re.compile('(All gowns|We recommend|See fit guide).*')
    brand_re = re.compile(r'By (.*)')
    gender_map = {'groom': 'men', 'girl': 'girls'}
    merch_re = re.compile('(Online exclusive|A BHLDN exclusive)')


class BhldnParseSpider(BaseParseSpider, Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-parse'
    price_css = '.price::text'

    def parse(self, response):
        sku_id = self.product_id(response)

        if response.css('.moredetails-link'):
            return
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        if self.is_homeware(garment['url_original']):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.gender(garment['url_original'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)
        if garment['trail']:
            garment['trail'] = self.add_trail(response)
        garment['category'] = self.category(garment['trail'])

        return garment

    def category(self, trail):
        categories = []

        for category in trail:
            if category[0]:
                categories.append(category[0])

        return categories

    def is_homeware(self, url):
        return 'decor' in url

    def merch_info(self, response):
        merch_info = []
        for rd in self.raw_description(response):
            if re.match(self.merch_re, rd):
                merch_info.append(rd)
        return merch_info + clean(response.css('.product-form__unavailable p::text'))


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
            if not re.match(self.unwanted_description_re, rd):
                raw_description.append(rd)

        return raw_description

    def raw_description(self, response):
        return clean(response.css('div[itemprop=description] ::text'))

    def product_brand(self, response):
        description = self.raw_description(response)

        for entry in description:
            re_groups = re.match(self.brand_re, entry)
            if re_groups:
                return re_groups.group(1)

        return 'bhldn'

    def image_urls(self, response):
        return clean(response.css('.js-bigimage::attr(href)'))

    def color(self, response):
        color_id = clean(response.css('option[selected]::attr(value)'))[0]
        color = json.loads(
            clean(response.css('option[value="' + color_id + '"]::attr(data-color)'))[0])

        return color['NAME'], color_id

    def skus(self, response):
        color, color_id = self.color(response)
        raw_skus = response.css(
            'select[data-color*="' + color_id + '"] option')[1:]
        skus = {}

        for raw_sku in raw_skus:
            availability = self.sku_availability(raw_sku)
            pre_order = self.sku_preorder(raw_sku)
            sku_id = clean(raw_sku.css('option::attr(value)'))[0]
            pricing = self.product_price(raw_sku)
            size = clean(raw_sku.css('option::text'))[0]
            sku = {'colour': color, 'size': size}

            if not availability:
                sku['out_of_stock'] = True

            if pre_order:
                sku['merch_info'] = pre_order

            sku.update(pricing)
            skus[sku_id] = sku

        return skus

    def product_price(self, raw_sku):
        saleprice = json.loads(
            clean(raw_sku.css('option::attr(data-saleprice)'))[0])['SALEPRICE']
        price = json.loads(
            clean(raw_sku.css('option::attr(data-price)'))[0])['PRICE']

        return self.product_pricing_common_new('', money_strs=[saleprice, price])

    def sku_availability(self, raw_sku):
        css = 'option::attr(data-availability)'
        availability = json.loads(clean(raw_sku.css(css))[0])

        return availability['STATUS'] == 'instock'

    def sku_preorder(self, raw_sku):
        css = 'option::attr(data-back-ordered)'
        preorder = json.loads(clean(raw_sku.css(css))[0])
        return preorder['MESSAGE']

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

    products_le = LinkExtractor(restrict_css=product_css)

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
             Rule(products_le, callback='parse_item'))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, priority=1, callback=self.parse_girls_men)

        yield Request(url='http://www.bhldn.com/', priority=-1, callback=self.parse)

    def parse_girls_men(self, response):
        for product in self.products_le.extract_links(response):
            yield Request(url=product.url, priority=1, callback=self.parse_item)
