import json
import re
from future.moves import itertools
from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import clean
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser
from skuscraper.spiders.base import SORTED_COLOURS


class Mixin:
    allowed_domains = ["www.loadednz.com"]
    start_urls = ['http://www.loadednz.com/products/outlet']
    market = 'NZ'
    retailer = 'loaded-nz'


class LoadedNzParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = '//*[contains(@class, "price")]//text()'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        if self.out_of_stock(response):
            garment['out_of_stock'] = True
            prev_price, price, currency = self.product_pricing(response)
            currency = self._CURRENCY_REMAP.get((self.market, currency), currency)
            garment['price'] = price
            garment['currency'] = currency
            if prev_price:
                garment['previous_prices'] = [prev_price]
        garment['skus'] = self.skus(response)
        return garment

    def image_urls(self, response):
        return clean(response.css('.image-grid img::attr(src)'))

    def skus(self, response):
        sizes = clean(response.css('select[name=size] > option::attr(value)'))
        prev_price, price, currency = self.product_pricing(response)
        currency = self._CURRENCY_REMAP.get((self.market, currency), currency)
        color = self.product_color(response)
        out_of_stock = self.out_of_stock(response)
        if not sizes:
            sizes = [self.one_size]
        skus = {}
        common_sku = {
            'color': color,
            'price': price,
            'currency': currency,
        }
        if prev_price:
            common_sku['previous_prices'] = [prev_price]
        if out_of_stock:
            common_sku['out_of_stock'] = True
        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size
            sku_id = '{}_{}'.format(color, size).replace(' ', '_')
            skus[sku_id] = sku
        return skus

    def product_id(self, response):
        return response.url.split('/')[-1]

    def product_brand(self, response):
        return clean(response.css('p.brand::text'))[0]

    def product_name(self, response):
        name = clean(response.css('p.style::text'))[0]
        brand = self.product_brand(response)
        p = re.compile('{}\s*'.format(brand), re.IGNORECASE)
        return re.sub(p, '', name)

    def raw_description(self, response):
        return clean(response.css('div.alt > div > div::text'))

    def product_description(self, response):
        return [d for d in self.raw_description(response) if not self.care_criteria(d)]

    def product_care(self, response):
        return [d for d in self.raw_description(response) if self.care_criteria(d)]

    def product_category(self, response):
        return response.request.meta.get('category')

    def product_gender(self, response):
        return response.request.meta.get('gender')

    def product_color(self, response):
        color = response.css('p.colour::text').extract_first()
        if not color:
            name = self.product_name(response)
            colors = [match.group(0) for match in
                      [re.search('({})'.format(color), name)
                       for color in SORTED_COLOURS]
                      if match]
            return ','.join(colors) if colors else color

    def out_of_stock(self, response):
        return not response.css("form[action='/add-to-cart']")


class LoadedNzCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LoadedNzParseSpider()
    base_url = 'http://www.loadednz.com/products'

    listing_css = [
        ".navbar-nav",
        ".text-right"
    ]

    product_css = [
        ".image"
    ]

    rules = (Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))

    def parse(self, response):
        categories = clean(response.css('select[name=category] > option::attr(value)'))
        brands = clean(response.css('select[name=brand] > option::attr(value)'))
        genders = clean(response.css('select[name=gender] > option::attr(value)').extract())
        tree = itertools.product(categories, brands, genders)
        for category, brand, gender in tree:
            meta = {
                'category': [category],
                'gender': gender[:-1],
                'trail': self.add_trail(response),
            }
            url = '{}/{},{},{}'.format(self.base_url, brand, category, gender)
            yield Request(url=url, meta=meta, callback=super(LoadedNzCrawlSpider,self).parse)

