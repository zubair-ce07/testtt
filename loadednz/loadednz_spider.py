import json
import re
from future.moves import itertools
from scrapy.http.request import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import clean
from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser


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
        garment['skus'] = self.skus(response)
        if not garment['skus']:
            garment['out_of_stock'] = True
        return garment

    def image_urls(self, response):
        return clean(response.css('.image-grid img::attr(src)'))

    def skus(self, response):
        sizes = clean(response.css('select[name=size] > option::attr(value)'))
        prev_price, price, currency = self.product_pricing(response)
        currency = 'NZD'
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

    def product_pricing(self, response):
        prev_price, price, currency = super(LoadedNzParseSpider, self).product_pricing(response)
        original_price_css = 'p.price > span.original::text'
        original = clean(response.css(original_price_css))
        if original:
            price_string = original[0]
            currency, prev_price = CurrencyParser.currency_and_price(price_string)
        return (prev_price, price, currency) if prev_price != price else (None, price, currency)

    def product_id(self, response):
        return response.css('input[name=sku]::attr(value)').extract_first()

    def product_brand(self, response):
        return response.request.meta.get('brand')

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
            return self.detect_colour(self.product_name(response))
        return color

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
        for request in self.search_requests(categories, brands, genders):
            request.meta['trail'] = self.add_trail(response)
            yield request

    def search_requests(self, categories, brands, genders):
        tree = itertools.product(categories, brands, genders)
        for category, brand, gender in tree:
            meta = {
                'category': [category],
                'brand': brand,
                'gender': gender,
            }
            url = '{}/{},{},{}'.format(self.base_url, brand, category, gender)
            yield Request(url=url, meta=meta, callback=self.parse_search_result)

    def parse_search_result(self, response):
        requests = super(LoadedNzCrawlSpider, self).parse(response)
        for request in requests:
            request.meta['brand'] = response.meta.get('brand')
            yield request

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(('scrapy parse --spider loaded-nz-parse http://www.loadednz.com/products/jansport/jansport-x-i-love-ugly-iron-sight/JSOAT75R0ZQ_CHAGRY').split())
    # cmdline.execute('scrapy crawl loaded-nz-crawl'.split())
