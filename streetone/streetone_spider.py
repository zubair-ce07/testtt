import re
import json
import time
from scrapy.http.request import Request
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, CurrencyParser, clean


class Mixin:
    name = "street-one-de"
    allowed_domains = ["street-one.de"]
    retailer = 'street-one-de'
    market = 'DE'
    lang = 'de'
    start_urls = ['http://street-one.de/']


class StreetOneParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    image_url_re = re.compile('aZoom\[\d+\].*?\"(.*)\"', re.MULTILINE)

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        product = self.raw_product(response)
        garment['gender'] = 'women'
        garment['brand'] = 'Street One'
        garment['image_urls'] = self.product_images(response)
        garment['skus'] = self.skus(response, product)
        return garment

    def raw_product(self, response):
        json_raw = clean(response.css('script[type="application/ld+json"]::text'))[0]
        return json.loads(json_raw)

    def product_name(self, response):
        return clean(response.css('dd.second > h1::text'))[0]

    def product_category(self, response):
        category_css = 'ul.trail-line li:not(li:first-child) a::text'
        return clean(response.css(category_css))

    def product_currency(self, product):
        return product['offers']['priceCurrency']

    def product_care(self, response):
        detail_css = '#cbr-details-info li:last-child'
        material = self.text_from_html(clean(response.css(detail_css))[0])
        care_css = 'p.care_instruction_text > span::text'
        care_instructions = clean(response.css(care_css))
        return material + care_instructions + [d for d in self.description_raw(response)
                                               if self.care_criteria(d)]

    def product_description(self, response):
        desc = self.description_raw(response)
        return [d for d in desc if not self.care_criteria(d)]

    def description_raw(self, response):
        short_desc = clean(response.css('meta[name="description"]::attr(content)'))
        long_desc = clean(response.css('div.produkt-infos div#cbr-details-info'))[0]
        long_desc = self.text_from_html(long_desc)
        return short_desc.extend(long_desc) or short_desc

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

    def skus(self, response, product):
        skus = {}
        price = self.product_price(product)
        color = self.product_color(response)
        currency = self.product_currency(product)
        available_sizes = self.available_sizes(response)
        out_of_stock = self.out_of_stock_sizes(response)
        sizes = available_sizes if available_sizes else []
        sizes += out_of_stock if out_of_stock else []
        if not sizes:
            return
        size_details = self.size_details(response)
        sku_common = {}
        sku_common['colour'] = color
        sku_common['currency'] = currency
        for size in sizes:
            price = size_details[size]['price'] if size in size_details else price
            sku = sku_common.copy()
            sku['size'] = size
            sku['price'] = CurrencyParser.lowest_price(price)
            if size in out_of_stock:
                sku['out_of_stock'] = True
            skus[color + '_' + size] = sku

        return skus

    def size_details(self, response):
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
            sizes= re.sub('\(|\)|\'', '', sizes).split(',')
            return sizes
        return None

    def out_of_stock_sizes(self, response):
        script = response.css('script:contains("var attr")')
        values_0 = script.re_first('values\[0\] = new Array([^;]*)')
        values_1 = script.re_first('values\[1\] = new Array([^;]*)')
        out_of_stock = []
        pattern = re.compile('\(|\)|\'')
        if values_0 and values_1:
            values_0 = pattern.sub('', values_0).split(',')
            values_1 = pattern.sub('', values_1).split(',')
            all_sizes = [size_0 + '_' + size_1
                         for size_0 in values_0
                         for size_1 in values_1]
            available_sizes = script.re_first('sizes = new Array([^;]*)')
            available_sizes = pattern.sub('', available_sizes).split(',')
            out_of_stock = list(set(all_sizes) - set(available_sizes))
        elif values_0:
            values_0 = pattern.sub('', values_0).split(',')
            available_sizes = script.re_first('sizes = new Array([^;]*)')
            available_sizes = pattern.sub('',
                                     available_sizes).split(',')
            out_of_stock = list(set(values_0) - set(available_sizes))
        return out_of_stock

    def format_sku_price(self, price):
        return str(price).split()[0].replace('.','').replace(',','')

    def product_price(self, product):
        return CurrencyParser.conversion(product['offers']['price'])

    def product_images(self, response):
        return response.css('script:contains("aZoom")').re(self.image_url_re)

    def is_sale(self, response):
        return response.css('span.linethrough')

    def previous_price(self, response):
        prev_price = response.css('span.linethrough::text').re_first('(\d+,\d+)')
        return CurrencyParser.conversion(prev_price)


class StreetOneCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = StreetOneParseSpider()
    listing_css = ['.mainnavigation', '#sidenavigation']
    product_css = ['li.produkt-bild']

    def process_pagination_link(link):
        results = re.findall('ecs_jump\((\d+)\)', link)
        if results:
            page = results.pop()
            return '?page='+page+'&ajax=1'

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.produkte-pagination', attrs='onclick',
                           process_value=process_pagination_link), callback='parse')
    ]

