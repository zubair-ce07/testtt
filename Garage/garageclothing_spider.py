from copy import deepcopy
import re

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, FormRequest

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'garageclothing-ca'
    market = 'CA'
    allowed_domains = ['garageclothing.com', 'dynamiteclothing.com']
    gender = 'women'


class GarageclothingParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    size_api_url = 'https://www.garageclothing.com/ca/prod/include/productSizes.jsp'
    image_api_url = 'https://www.garageclothing.com/ca/prod/include/pdpImageDisplay.jsp'
    price_css = '.prodPricePDP ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['gender'] = self.gender
        garment['image_urls'] = []
        garment['meta'] = {
            'requests_queue': self.image_and_colour_requests(response, garment),
            'pricing': self.product_pricing_common_new(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        css = '.size:not([stocklevel="0"])'
        colour = response.meta['colorname']

        for size_sel in response.css(css):
            sku = deepcopy(response.meta['garment']['meta']['pricing'])
            sku['colour'] = colour
            sku['size'] = self.one_size if clean(size_sel.css('::attr(size)'))[0] == 'O/S' else clean(size_sel.css('::attr(size)'))[0]

            sku_id = clean(size_sel.css('::attr(skuid)'))[0]
            skus.update({sku_id: sku})

        return skus

    def image_and_colour_requests(self, response, garment):
        css = '#prodDetailSwatch [colourid]'
        product_id = garment['retailer_sku']
        requests = []
        original_style = clean(response.css('#originalStyle::attr(value)'))

        form_data = {
            'productId': product_id,
        }

        for colour_sel in response.css(css):
            form_data['colour'] = clean(colour_sel.css('::attr(colourid)'))[0]

            if original_style:
                form_data['originalStyle'] = original_style[0]

            colorname = clean(colour_sel.css('::attr(colorname)'))[0]
            requests += [FormRequest(url=self.size_api_url, callback=self.parse_colour, dont_filter=True, formdata=form_data, meta={'colorname': colorname}),
                         FormRequest(url=self.image_api_url, callback=self.parse_images, dont_filter=True, formdata=form_data)]

        return requests

    def product_id(self, response):
        id_css = '[name="productId"]::attr(value)'
        return clean(response.css(id_css))[0].replace('Style # ', '')

    def image_urls(self, response):
        css = '#additionalViewsPDP .thumbImageSelectorPDP::attr(src)'
        return clean(response.css(css))

    def product_name(self, response):
        css = '.prodName::text'
        return clean(response.css(css))[0]

    def product_description(self, response):
        css = '#descTab0Content ::text'
        return clean(response.css(css))

    def product_care(self, response):
        css = '#descTab1Content li::text'
        return [x for x in clean(response.css(css)) if self.care_criteria_simplified(x)]

    def product_category(self, response):
        css = '.shopParentCategory::text'
        return clean(response.css(css))[0].replace('>', '')


class GarageclothingCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = GarageclothingParseSpider()
    cookie_url = 'https://www.dynamiteclothing.com/?canonicalSessionRenderSessionId=true'
    session_regex = re.compile('JSESSIONID=([a-zA-Z0-9.]+);')
    handle_httpstatus_list = [404]

    listing_css = [
        '#mainCategoryMenu',
        '#catPageNext'
    ]

    product_css = '.prodListingImg .none'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css,), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css,), callback='parse_item'),
    )

    def start_requests(self):
        yield Request(url=self.cookie_url, callback=self.parse_session_cookie)

    def parse_session_cookie(self, response):
        jsession_id = self.session_regex.search(response.headers['Set-Cookie'].decode()).group(1)
        yield Request('https://www.garageclothing.com/ca/', cookies={'JSESSIONID': jsession_id})

