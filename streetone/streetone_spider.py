import re
import json
from scrapy.spiders.crawl import Rule
from scrapy.linkextractors import LinkExtractor
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, CurrencyParser, clean


class Mixin:
    name = "street-one-de"
    allowed_domains = ["street-one.de"]
    retailer = 'street-one-de'
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
        raw_product = self.raw_product(response)
        garment['image_urls'] = self.product_images(response)
        if self.out_of_stock(raw_product):
            garment['out_of_stock'] = True
            prev_price, garment['price'], garment['currency'] = self.product_pricing(response, raw_product)
            if prev_price:
                garment['previous_prices'] = [prev_price]
        else:
            garment['skus'] = self.skus(response, raw_product)
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
        category_css = '#trail li:not(li:first-child) a'
        return clean(response.css(category_css).xpath('text()'))

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
        return color[0].replace(' ', '_') if color else self.color_from_url(response)

    def color_from_url(self, response):
        url = response.url
        url = url.split('/')[-1].split('.')[0]
        name = self.product_name(response).strip().replace(' ', '-')
        if name in url:
            return url.replace(name, '').lstrip('-').replace('-', '_')

    def product_pricing(self, response, product):
        price = CurrencyParser.conversion(product['offers']['price'])
        prev_price_css = 'span.linethrough::text'
        prev_price = response.css(prev_price_css).re_first('(\d+,\d+)')
        if prev_price:
            prev_price = CurrencyParser.conversion(response.css(prev_price_css).re_first('(\d+,\d+)'))
        currency = product['offers']['priceCurrency']
        return prev_price, price, currency

    def skus(self, response, product):
        skus = {}
        variants = self.all_sizes(response) or self.one_size
        available = self.available_sizes(response) or []
        if not variants:
            return {}
        size_info = self.variant_info(response)
        sku_common = {}
        prev_price, sku_common['price'], sku_common['currency'] = self.product_pricing(response, product)
        sku_common['colour'] = self.product_color(response)
        for size in variants:
            sku = sku_common.copy()
            sku['size'] = size
            if size in available:
                price = size_info[size]['price']
                if isinstance(price, str):
                    sku['price'] = CurrencyParser.lowest_price(price)
                else:
                    sku['price'] = CurrencyParser.float_conversion(price)
            if prev_price:
                sku['previous_prices'] = [prev_price]
            if size not in available:
                sku['out_of_stock'] = True
            skus[sku['colour'] + '_' + size] = sku
        return skus

    def variant_info(self, response):
        details = {}
        script = response.css('script:contains("var attr")')
        if not script:
            return details
        results = re.findall('eval\(\((\{.*\})\)\)', clean(script)[0])
        if not results:
            return {}
        raw = results.pop()
        return json.loads(raw)

    def available_sizes(self, response):
        script = response.css('script:contains("var attr")')
        sizes = script.re_first('sizes = new Array([^;]*)')
        if sizes:
            sizes = self.to_list(sizes)
            return sizes
        return None

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

    def is_sale(self, response):
        return response.css('span.linethrough')

    def out_of_stock(self, product):
        return False


class StreetOneCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = StreetOneParseSpider()
    listing_css = ['.mainnavigation', '#sidenavigation']
    product_css = ['li.produkt-bild']

    def parse_pagination(link):
        results = re.findall('ecs_jump\((\d+)\)', link)
        if results:
            page = results.pop()
            return '?page='+page+'&ajax=1'

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.produkte-pagination', attrs='onclick',
                           process_value=parse_pagination), callback='parse')
    ]
