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

    brand_re = re.compile('(.*)/')

    price_css = '#itemD_mwControl .pMedium::text, .priceB::text'
    previous_price_re = re.compile('(¥.*)')

    sold_out = '売り切れ'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['gender'] = self.product_gender(response)

        requests = self.colour_requests(response) or self.colour_stock_requests(response) or self.size_requests(response)

        if not requests:
            garment['skus'] = self.one_size_skus(response)

            return garment

        garment['meta'] = {
            'requests_queue': requests,
            'pricing': self.product_pricing_common_new(response, post_process=self.clean_money)
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
        skus[self.one_size].update(self.product_pricing_common_new(response, post_process=self.clean_money))

        return skus

    def skus(self, response):
        raw_sku = json.loads(clean(response.text))['Result']

        size = response.meta.get('size', self.one_size)
        colour = response.meta.get('colour', '')
        sku = {'size': size}

        if colour:
            sku['colour'] = colour

        if raw_sku['data'][0]['zaiko'] == self.sold_out:
            sku['out_of_stock'] = True

        sku.update(response.meta['garment']['meta']['pricing'])

        return {colour+'_'+size: sku}

    def request_id(self, response):
        request_id = clean(response.css('[name="MOSHBG"]::attr(value)'))

        return response.meta.get('request_id', request_id[0] if request_id else '')

    def size_variants(self, response):
        sizes = clean(response.css('.size li [type="radio"]::attr(value)'))

        if response.css('.size, .color'):
            return sizes

        return [size['namec2'] for size in json.loads(clean(response.text))['Result'].get('cls2', [])]

    def size_requests(self, response):
        requests = []
        sizes = self.size_variants(response)

        meta = {}
        colour = response.meta.get('colour', '')

        if colour:
            meta['colour'] = colour

        colour_query_parameter = response.meta.get('colour_query_parameter', '')

        for size in sizes:
            size_query_parameter = urllib.parse.quote(size).replace('%', '%25')
            meta['size'] = size
            url = self.stock_api_url.format(
                request_id=self.request_id(response), colour=colour_query_parameter, size=size_query_parameter)
            requests += [FormRequest(url=url, meta=meta, callback=self.parse_sku)]

        return requests

    def colour_selectors(self, response):
        return response.css('.color li, .color option:not([value=""])')

    def colour_requests(self, response):
        request_id = self.request_id(response)
        colours = self.colour_selectors(response)
        sizes = self.size_variants(response)

        requests = []

        if not sizes and not response.css('.size'):
            return requests

        for colour_sel in colours:
            colour_name, colour_query_parameter = self.colour_name_and_query_parameter(colour_sel)
            meta = {'colour': colour_name, 'request_id': request_id, 'colour_query_parameter': colour_query_parameter}

            url = self.colour_request_url.format(request_id=request_id, colour=colour_query_parameter)
            requests += [FormRequest(url=url, meta=meta, callback=self.parse_colour)]

        return requests

    def colour_stock_requests(self, response):
        request_id = self.request_id(response)
        colours = self.colour_selectors(response)

        requests = []

        for colour_sel in colours:
            colour_name, colour_query_parameter = self.colour_name_and_query_parameter(colour_sel)
            meta = {'colour': colour_name, 'request_id': request_id, 'colour_query_parameter': colour_query_parameter}

            url = self.stock_api_url.format(request_id=request_id, colour=colour_query_parameter, size='')
            requests += [FormRequest(url=url, meta=meta, callback=self.parse_colour)]

        return requests

    def colour_name_and_query_parameter(self, colour_selector):
        colour_name = clean(colour_selector.css('::attr(title),::text'))[0]
        colour_value = clean(colour_selector.css(' [type="radio"]::attr(value),::attr(value)'))[0]
        colour_query_parameter = urllib.parse.quote(colour_value).replace('%', '%25')

        return colour_name, colour_query_parameter

    def product_gender(self, response):
        soup = [self.raw_name(response) + response.url] + self.product_category(response)
        soup += [url for t, url in response.meta.get('trail', [])]
        soup = ' '.join(soup)

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        return clean(response.css('#dpvThumb li::attr(data-dpv-expand-url)'))

    def clean_money(self, money_strs):
        return sum([self.previous_price_re.findall(money_str) for money_str in money_strs], [])

    def product_id(self, response):
        return clean(response.css('#vs-product-id::attr(value)'))[0]

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"] ::text'))[0]

    def product_category(self, response):
        return clean(response.css('[itemprop="category"] [itemprop="title"]::text'))[1:]

    def product_brand(self, response):
        brand = self.brand_re.findall(self.raw_name(response))

        return brand[0] if brand else 'Dinos'

    def product_name(self, response):
        return self.raw_name(response).replace(self.product_brand(response)+'/', '')

    def raw_description(self, response):
        return clean(response.xpath('//*[contains(@id, "itemtable")]/tbody/tr[1]/td/text()'))

    def product_description(self, response):
        css = '.itemD_itemGuide ::text, [itemprop="description"] ::text'
        description = clean(response.css(css))

        return description + [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        care = clean(response.css('.itemD_featureBox ::text'))

        return care + [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]


class DinosCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = DinosParseSpider()

    pagination_css = '.btn.next'

    product_css = '.picPreview'

    rules = (
        Rule(LinkExtractor(restrict_css=pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css),
             callback='parse_item'),
    )
