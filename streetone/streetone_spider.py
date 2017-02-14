import json

import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule

from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, CurrencyParser, clean


class Mixin:
    allowed_domains = ["street-one.de"]
    retailer = 'streetone-de'
    market = 'DE'
    lang = 'de'
    gender = 'women'
    start_urls = ['http://street-one.de/']


class StreetOneParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_url_re = re.compile('aZoom\[\d+\].*?\"(.*)\"', re.M)
    list_pattern_re = re.compile('\(|\)|\'')

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        product = self.raw_product(response)
        garment['image_urls'] = self.product_images(response)
        if self.out_of_stock(product):
            garment['out_of_stock'] = True
            pricing = self.product_pricing_common(response, product)
            garment['price'] = pricing['price']
            garment['currency'] = pricing['currency']
            if pricing.get('previous_prices'):
                garment['previous_prices'] = pricing['previous_prices']
        else:
            garment['skus'] = self.skus(response, product)
        return garment

    def raw_product(self, response):
        script_re = 'script[type="application/ld+json"]::text'
        raw_script = clean(response.css(script_re))[0]
        return json.loads(raw_script)

    def product_brand(self, response):
        return 'Street One'

    def product_name(self, response):
        return clean(response.css('dd.second > h1::text'))[0]

    def product_category(self, response):
        category_css = '#trail li:not(li:first-child) a *::text'
        return clean(response.css(category_css))

    def product_care(self, response):
        care_css = 'p.care_instruction_text > span::text'
        care_instructions = clean(response.css(care_css))
        return care_instructions + [d for d in self.raw_description(response)
                                    if self.care_criteria(d)]

    def product_description(self, response):
        desc = self.raw_description(response)
        return [d for d in desc if not self.care_criteria(d)]

    def raw_description(self, response):
        css = 'meta[name="description"]::attr(content), #cbr-details-info *::text'
        return clean(response.css(css))

    def product_id(self, response):
        id_css = 'script:contains("ScarabQueue.push")'
        return response.css(id_css).re_first("push\(\['view',\s*'(.+)'")

    def product_color(self, response):
        color_css = 'ul.farbe > li.active span.tool-tip > span::text'
        color = clean(response.css(color_css))
        return color[0] if color else self.color_from_url(response)

    def color_from_url(self, response):
        # http://www.street-one.de/All-Styles/Pullover-Strickjacken/Pullover/Rundhalspullover/Pulli-mit-Struktur-Felicitas-off-white.html
        url = response.url.split('/')[-1].split('.')[0]
        name = self.product_name(response).strip().replace(' ', '-')
        if name in url:
            return url.replace(name, '').lstrip('-')

    def product_pricing_common(self, response, product):
        pricing = {}
        pricing['price'] = CurrencyParser.conversion(product['offers']['price'])
        prev_price = response.css('span.linethrough::text')
        if prev_price:
            pricing['previous_prices'] = CurrencyParser.lowest_price(clean(prev_price)[0])
        pricing['currency'] = product['offers']['priceCurrency']
        return pricing

    def skus(self, response, product):
        skus = {}
        variants = self.all_sizes(response) or self.one_size
        available = self.available_sizes(response)
        size_info = self.variant_info(response)
        sku_common = self.product_pricing_common(response, product)
        sku_common['colour'] = self.product_color(response)
        for size in variants:
            sku = sku_common.copy()
            sku['size'] = size
            price = size_info.get(size, sku)['price']
            if isinstance(price, str):
                sku['price'] = CurrencyParser.lowest_price(price)
            else:
                sku['price'] = CurrencyParser.float_conversion(price)
            if size not in available:
                sku['out_of_stock'] = True
            sku_id = '{}_{}'.format(sku['colour'].replace(' ','/'), size)
            skus[sku_id] = sku
        return skus

    def variant_info(self, response):
        script = clean(response.css('script:contains("var attr")'))
        results = re.findall('eval\(\((\{.*\})\)\)', script[0] if script else '')
        return json.loads(results[0]) if results else {}

    def available_sizes(self, response):
        script = response.css('script:contains("var attr")')
        return self.to_list(script.re_first('sizes = new Array([^;]*)'))

    def all_sizes(self, response):
        script = response.css('script:contains("var attr")')
        widths = self.to_list(script.re_first('values\[0\] = new Array([^;]*)'))
        lengths = self.to_list(script.re_first('values\[1\] = new Array([^;]*)'))
        if widths and lengths:
            return ['{}_{}'.format(w, l) for w in widths for l in lengths]
        return [w for w in widths]

    def to_list(self, s):
        return self.list_pattern_re.sub('', s).split(',') if s else []

    def product_images(self, response):
        return response.css('script:contains("aZoom")').re(self.image_url_re)

    def out_of_stock(self, product):
        return 'InStock' not in product['offers']['availability']


class StreetOneCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = StreetOneParseSpider()
    listing_css = ['.mainnavigation', '#sidenavigation']
    product_css = ['li.produkt-bild']
    pagination_css = ['.produkte-pagination']

    def parse_pagination(link):
        results = re.findall('ecs_jump\((\d+)\)', link)
        if results:
            page = results.pop()
            return '?page='+page+'&ajax=1'

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=pagination_css, attrs='onclick',
                           process_value=parse_pagination), callback='parse')
    ]

