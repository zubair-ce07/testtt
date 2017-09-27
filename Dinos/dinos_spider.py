import re
import json
import urllib.parse

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'dinos-jp'
    lang = 'ja'
    market = 'JP'
    allowed_domains = ['dinos.co.jp']
    start_urls = [
        'https://www.dinos.co.jp/c2/002003/',
        'https://www.dinos.co.jp/c2/002009/',
        'https://www.dinos.co.jp/c3/002003011/1a1/',
        'https://www.dinos.co.jp/c3/002010003/1a1/',
        'https://www.dinos.co.jp/c4/002010025005/1a2/',
        'https://www.dinos.co.jp/c4/002010025009/1a2/',
        'https://www.dinos.co.jp/c4/002010025010/1a2/',
        'https://www.dinos.co.jp/c4/002010025011/1a2/',
        'https://www.dinos.co.jp/c4/002010025018/1a2/',
        'https://www.dinos.co.jp/c3/002003005/1a1/',
        'https://www.dinos.co.jp/c3/002009016/1a1/',
        'https://www.dinos.co.jp/c4/002010025005/1a2/',
        'https://www.dinos.co.jp/c4/002010025009/1a2/',
        'https://www.dinos.co.jp/c4/002010025010/1a2/',
        'https://www.dinos.co.jp/c4/002010025011/1a2/',
        'https://www.dinos.co.jp/c4/002010025018/1a2/',
        'https://www.dinos.co.jp/p/1367100493/?id=002010025009___1513545',
        'https://www.dinos.co.jp/p/1367100492/?id=002010025009___1513544'
    ]


class DinosParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    stock_api_url = 'https://www.dinos.co.jp/defaultMall/sitemap/XHRGetZaikoInfo.jsp' \
                    '?GOODS_NO=&MOSHBG={request_id}&CLS1CD={colour}&CLS2CD={size}'

    colour_request_url = 'https://www.dinos.co.jp/defaultMall/sitemap/XHRGetGoodsCls2.jsp' \
                        '?CATNO=900&MOSHBG={request_id}&CLS1CD={colour}'

    gender_map = [
        ('ガールズ', 'girls'),
        ('ボーイズ', 'boys'),

        ('メンズ', 'men'),
        ('002003005', 'men'),
        ('002009016', 'men'),

        ('002010025005', 'unisex-kids'),
        ('002010025009', 'unisex-kids'),
        ('002010025010', 'unisex-kids'),
        ('002010025011', 'unisex-kids'),
        ('002010025018', 'unisex-kids'),
    ]

    brands_map = [
        ('ポロ・ラルフローレン', 'Polo · Ralph Lauren'),
        ('miki HOUSE', 'MIKI HOUSE double B'),
        ('miki HOUSE/ミキハウス ダブルB', 'MIKI HOUSE double B'),
        ('ミキハウス ダブルB', 'MIKI HOUSE double B'),
        ('Tom Chris', 'Tom Chris'),
        ('ハロルル', 'hellolulu'),
        ('hellolulu', 'hellolulu'),
        ('インビクタ', 'INVISTA'),
        ('ロゴス', 'LOGOS'),
        ('LOGOS', 'LOGOS'),
        ('adidas', 'Adidas'),
        ('アディダス', 'Adidas'),
        ('VARCO', 'VARCO'),
        ('WATER ZERO', 'WATER ZERO'),
        ('NEOPRO RED', 'NEOPRO RED'),
        ('A. L. I & CORDURA®', 'A. L. I & CORDURA®'),
        ('MIZUNO', 'MIZUNO'),
        ('ミズノ', 'MIZUNO'),
        ('MIZUNO', 'MIZUNO'),
        ('ace', 'ace'),
        ('Champion', 'Champion'),
        ('PEANUTS・SNOOPY', 'PEANUTS・SNOOPY'),
        ('BENETTON', 'BENETTON'),
        ('REEBOK', 'REEBOK'),
        ('Mizutori of Buddha', 'Mizutori of Buddha'),
        ('Miki House DoubleB', 'Miki House DoubleB'),
        ('レッシグ', 'Laessig'),
        ('Laessig', 'Laessig')
    ]

    brand_re = re.compile('([［］/.])')

    price_css = '#itemD_mwControl .pMedium::text, .priceB::text'
    previous_price_re = re.compile('(¥.*)')

    sold_out = '売り切れ'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)

        requests = self.colour_requests(response) or \
            self.colour_stock_requests(response) or \
            self.size_requests(response)

        if not requests:
            garment['skus'] = self.one_size_skus(response)

            return garment

        garment['meta'] = {
            'requests_queue': requests,
            'pricing': self.product_pricing_common_new(
                response, post_process=self.clean_money)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        requests = self.size_requests(response)

        if not requests:
            garment['skus'].update(self.skus(response))

        garment['meta']['requests_queue'] += requests

        return self.next_request_or_garment(garment)

    def parse_sku(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def one_size_skus(self, response):
        skus = {
            self.one_size: {'size': self.one_size}
        }
        skus[self.one_size].update(
            self.product_pricing_common_new(
                response, post_process=self.clean_money))

        return skus

    def skus(self, response):
        raw_sku = json.loads(clean(response.text))['Result']

        size = response.meta.get('size') or self.one_size
        colour = response.meta.get('colour', '')
        sku = {'size': size}

        if colour:
            sku['colour'] = colour

        if raw_sku['data'][0]['zaiko'] == self.sold_out:
            sku['out_of_stock'] = True

        sku.update(response.meta['garment']['meta']['pricing'])

        return {colour+'_'+size: sku}

    def request_id(self, response):
        css = '[name="MOSHBG"]::attr(value)'
        request_id = clean(response.css(css))

        url = urllib.parse.urlparse(response.url)
        url_query = dict(urllib.parse.parse_qsl(url.query))

        return url_query.get('MOSHBG') or request_id[0]

    def size_variants(self, response):
        css = '.size li [type="radio"]::attr(value)'
        sizes = clean(response.css(css))

        if response.css('#itemD_mainWrap'):
            return sizes

        sizes = json.loads(clean(response.text))['Result'].get('cls2', [])

        return [size['namec2'] for size in sizes]

    def size_requests(self, response):
        requests = []
        sizes = self.size_variants(response)

        meta = {}
        colour = response.meta.get('colour', '')

        if colour:
            meta['colour'] = colour

        url = urllib.parse.urlparse(response.url)
        url_query = dict(urllib.parse.parse_qsl(url.query))

        colour_query_parameter = url_query.get('CLS1CD', '').replace('%', '%25')

        for size in sizes:
            meta['size'] = size
            size_query_parameter = urllib.parse.quote(size).replace('%', '%25')

            url = self.stock_api_url.format(
                request_id=self.request_id(response),
                colour=colour_query_parameter,
                size=size_query_parameter)

            requests += [FormRequest(url=url, meta=meta, callback=self.parse_sku)]

        return requests

    def colour_selectors(self, response):
        css = '.color li, .color select [value]:not([value=""])'
        
        return response.css(css)

    def colour_requests(self, response):
        request_id = self.request_id(response)
        colours = self.colour_selectors(response)

        requests = []

        if not response.css('.size'):
            return requests

        for colour_sel in colours:
            colour_name, colour_query_parameter = self.colour_name_and_query_parameter(colour_sel)
            meta = {'colour': colour_name}

            url = self.colour_request_url.format(
                request_id=request_id,
                colour=colour_query_parameter)

            requests += [FormRequest(url=url, meta=meta, callback=self.parse_colour)]

        return requests

    def colour_stock_requests(self, response):
        request_id = self.request_id(response)
        colours = self.colour_selectors(response)

        requests = []

        for colour_sel in colours:
            colour_name, colour_query_parameter = self.colour_name_and_query_parameter(colour_sel)

            meta = {'colour': colour_name}

            url = self.stock_api_url.format(
                request_id=request_id,
                colour=colour_query_parameter,
                size='')
            
            requests += [FormRequest(url=url, meta=meta, callback=self.parse_colour)]

        return requests

    def colour_name_and_query_parameter(self, colour_selector):
        name_css = '::attr(title),::text'
        value_css = ' [type="radio"]::attr(value),::attr(value)'

        colour_name = clean(colour_selector.css(name_css))[0]

        colour_code = clean(colour_selector.css(value_css))[0]
        colour_query_parameter = urllib.parse.quote(colour_code).replace('%', '%25')

        return colour_name, colour_query_parameter

    def product_gender(self, response):
        soup = [self.raw_name(response) + response.url] + self.product_category(response)
        soup += [url for _, url in response.meta.get('trail', [])]
        soup = ' '.join(soup)

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        css = '#dpvThumb li::attr(data-dpv-expand-url)'

        return clean(response.css(css))

    def clean_money(self, money_strs):
        nested_prev_prices = [self.previous_price_re.findall(money_str)
                              for money_str in money_strs]

        return sum(nested_prev_prices, [])

    def product_id(self, response):
        css = '#vs-product-id::attr(value)'

        return clean(response.css(css))[0]

    def raw_name(self, response):
        css = '[itemprop="name"] ::text'

        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '[itemprop="category"] [itemprop="title"]::text'

        return clean(response.css(css))[1:]

    def product_brand(self, response):
        raw_name = clean(self.raw_name(response))

        for brand_key, brand in self.brands_map:
            if brand_key in raw_name:
                return brand

        return 'Dinos'

    def product_name(self, response):
        raw_name = self.raw_name(response)

        for brand_key, brand in self.brands_map:
            raw_name = raw_name.replace(brand_key, '')

        return self.brand_re.sub('', raw_name)

    def raw_description(self, response):
        xpath = '//*[contains(@id, "itemtable")]/tbody/tr[1]/td/text()'

        return clean(response.xpath(xpath))

    def product_description(self, response):
        css = '.itemD_itemGuide ::text, [itemprop="description"] ::text'
        description = clean(response.css(css))

        description += [rd for rd in self.raw_description(response)
                        if not self.care_criteria_simplified(rd)]

        return description

    def product_care(self, response):
        css = '.itemD_featureBox ::text'
        care = clean(response.css(css))

        care += [rd for rd in self.raw_description(response)
                 if self.care_criteria_simplified(rd)]

        return care


class DinosCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DinosParseSpider()

    pagination_css = '.btn.next'

    product_css = '.picPreview'

    rules = (
        Rule(LinkExtractor(restrict_css=pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )
