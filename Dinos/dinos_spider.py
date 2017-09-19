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

    size_api_url = 'https://www.dinos.co.jp/defaultMall/sitemap/XHRGetGoodsCls2.jsp' \
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

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['gender'] = self.product_gender(response)

        requests = self.color_requests(response) or self.size_only_product_requests(response)

        if not requests:
            garment['skus'] = self.sku(response)
            return garment

        garment['meta'] = {
            'requests_queue': requests,
            'pricing': self.product_pricing_common_new(response, post_process=self.clean_money)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta.get('garment')
        garment['meta']['requests_queue'] += self.size_requests(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta.get('garment')
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def sku(self, response):
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

        if raw_sku['data'][0]['zaiko'] == '売り切れ':
            sku['out_of_stock'] = True

        sku.update(response.meta['garment']['meta']['pricing'])

        return {colour+'_'+size: sku}

    def size_requests(self, response):
        sizes = json.loads(clean(response.text))['Result']
        colour = response.meta.get('colour')
        colour_query_parameter = response.meta.get('colour_query_parameter')
        request_id = response.meta.get('request_id')
        meta = {
            'colour': colour
        }

        requests = []
        for size in sizes['cls2']:
            size_q = urllib.parse.quote(size['namec2']).replace('%', '%25')
            meta['size'] = size['valuec2']
            url = self.stock_api_url.format(request_id=request_id, colour=colour_query_parameter, size=size_q)
            requests += [FormRequest(url=url, meta=meta, callback=self.parse_size, dont_filter=True)]

        return requests

    def size_only_product_requests(self, response):
        requests = []

        if response.css('.color li'):
            return requests

        request_id = clean(response.css('[name="MOSHBG"]::attr(value)'))[0]
        sizes = clean(response.css('.size li [type="radio"]::attr(value)'))

        for size in sizes:
            size_q = urllib.parse.quote(size).replace('%', '%25')
            meta = {'size': size}
            url = self.stock_api_url.format(request_id=request_id, colour='', size=size_q)

            requests += [FormRequest(url=url, meta=meta, callback=self.parse_size, dont_filter=True)]

        return requests

    def color_requests(self, response):
        request_id = clean(response.css('[name="MOSHBG"]::attr(value)'))[0]
        colours = response.css('.color li')
        sizes = clean(response.css('.size li [type="radio"]::attr(value)'))
        requests = []

        callback = self.parse_size if not sizes else self.parse_colour

        for colour_sel in colours:
            colour_name, colour_query_parameter = self.colour_name_and_query_parameter(colour_sel)
            meta = {'colour': colour_name, 'request_id': request_id, 'colour_query_parameter': colour_query_parameter}

            url = self.size_api_url.format(request_id=request_id, colour=colour_query_parameter)

            if not sizes:
                url = self.stock_api_url.format(request_id=request_id, colour=colour_query_parameter, size='')

            requests += [FormRequest(url=url, meta=meta, callback=callback, dont_filter=True)]

        return requests

    def colour_name_and_query_parameter(self, colour_selector):
        colour_name = clean(colour_selector.css('::attr(title)'))[0]
        colour_value = clean(colour_selector.css(' [type="radio"]::attr(value)'))[0]
        colour_query_parameter = urllib.parse.quote(colour_value).replace('%', '%25')

        return colour_name, colour_query_parameter

    def product_gender(self, response):
        soup = self.raw_name(response) + ' '.join(self.product_category(response)) + \
               ' '.join(self.product_trail(response)) + response.url

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def product_trail(self, response):
        return [url for t, url in response.meta.get('trail', [])]

    def image_urls(self, response):
        return clean(response.css('#dpvThumb li::attr(data-dpv-expand-url)'))

    def clean_money(self, money_strs):
        price = money_strs[0]
        previous_price = self.previous_price_re.findall(money_strs[-1])

        return [price] + previous_price

    def product_id(self, response):
        return clean(response.css('#vs-product-id::attr(value)'))[0]

    def raw_name(self, response):
        return clean(response.css('[itemprop="name"] ::text'))[0]

    def product_category(self, response):
        return clean(response.css('[itemprop="category"] [itemprop="title"]::text'))[1:]

    def product_brand(self, response):
        brand = self.brand_re.findall(self.raw_name(response))

        return brand[0] if brand else ''

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
