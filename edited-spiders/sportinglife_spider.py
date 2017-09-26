import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean, remove_jsession


class Mixin:
    retailer = 'sportinglife-ca'
    lang = 'ca'
    market = 'CA'
    allowed_domains = [
        'sportinglife.ca'
    ]

    start_urls_with_meta = [
        ('https://www.sportinglife.ca/c/home', {'industry': 'homeware'}),
        ('https://www.sportinglife.ca/c/junior-girls-atheltic', {'gender': 'girls'}),
        ('https://www.sportinglife.ca/c/boys', {'gender': 'boys'}),
        ('https://www.sportinglife.ca/c/ladies', {'gender': 'women'}),
        ('https://www.sportinglife.ca/c/mens', {'gender': 'men'}),
        ('https://www.sportinglife.ca/c/footwear', {})
    ]


class SportingLifeParseSpider(BaseParseSpider, Mixin):
    take_first = TakeFirst()
    name = Mixin.retailer + '-parse'
    price_css = '#priceDisplay span::text'

    color_request_url_t = 'https://www.sportinglife.ca/json/sizePickerReloadResponse.jsp' \
                          '?productId={product_id}&colour={color}'
    image_url_t = 'https://www.sportinglife.ca/include/productDetailImage.jsp' \
                  '?prdId={product_id}&colour={color}'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment, response)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.sku_requests(response) + self.image_requests(response),
        }

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def parse_image(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        one_size = [{'size': self.one_size}]
        raw_sku = json.loads(response.text)
        for size in raw_sku.get('sizes', one_size):
            sku = response.meta['pricing'].copy()
            sku['size'] = size['size']

            if response.meta['color']:
                sku['color'] = response.meta['color']

            if self.out_of_stock(raw_sku, size):
                sku['out_of_stock'] = True

            sku_id = '{color}_{size}'.format(color=response.meta['color'], size=size['size'])
            skus[sku_id] = sku

        return skus

    def product_id(self, response):
        regex = '\"productID\": \"\d+\"|$'
        css = 'head [type="application/ld+json"]::text'
        return re.sub('productID|[:"\s]', '', response.css(css).re(regex)[0])

    def product_name(self, response):
        return self.take_first(clean(response.css('.product-detail-container h2::text')))

    def product_brand(self, response):
        return self.take_first(clean(response.css('.product-detail-container strong::text'))) or 'SportingLife'

    def product_category(self, response):
        return clean(response.css('.breadcrumb li a::text'))[1:]

    def product_color(self, response):
        return clean(response.css('.swatches img::attr(title)')) or ['']

    def image_requests(self, response):
        product_id = self.product_id(response)
        colors = self.product_color(response)
        return [Request(url=self.image_url_t.format(product_id=product_id, color=color), callback=self.parse_image)
                for color in colors]

    def image_urls(self, response, ):
        css = 'svg::attr(href)'
        return [response.urljoin(url) for url in clean(response.css(css))]

    def sku_requests(self, response):
        product_id = self.product_id(response)
        color_requests = []
        for color in self.product_color(response):
            color_requests.append(Request(url=self.color_request_url_t.format(product_id=product_id, color=color),
                                          callback=self.parse_skus,
                                          meta={'pricing': self.product_pricing_common_new(response),
                                                'color': color
                                                }))
        return color_requests

    def out_of_stock(self, raw_sku, raw_size):
        return not (raw_size.get('enabled') or raw_sku.get('singleSku', {'enabled': False})['enabled'])

    def raw_description(self, response):
        return clean(response.css('#tabs-details ::text'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def product_gender(self, garment, response):
        if response.meta.get('industry'):
            return

        gender = garment['gender']
        if gender:
            return gender

        soup = [garment['name']] + garment['category'] + [garment['url']]
        soup = ' '.join(soup).lower()

        for gender_str, gender in self.GENDER_MAP:
            if gender_str in soup:
                return gender

        return 'unisex-adults'


class SportingLifeCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SportingLifeParseSpider()

    listing_css = [
        '.parent .small-padding:not(.product-card)',
        '.pagination',
    ]
    products_css = '.product-card .image-container'

    deny_re = ['/equipment/',
               '/equipment-cylce/',
               '/home-accesories-toys/',
               ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_re, process_value=remove_jsession),
             callback='parse', ),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item', ),
    )
