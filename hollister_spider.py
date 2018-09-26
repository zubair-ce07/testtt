import json
from urllib.parse import urljoin

import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'hollister'
    image_api_url = 'http://anf.scene7.com/is/image/'


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    start_urls = [
        'http://www.hollisterco.jp/en_JP/guys-hollister-sale?icmp=ICT:BTS18:M:HP:B:P:POFF:SS:SeptWk4']
    allowed_domains = ['hollisterco.jp', 'anf.scene7.com']


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    start_urls = [
        'https://www.hollisterco.cn/en_CN/guys-tops-hoodies-and-sweatshirts?icmp=ICT:BTS18:M:HP:H:K:x:HDSWT:SeptWk2']
    allowed_domains = ['hollisterco.cn', 'anf.scene7.com']


class MixinHK(Mixin):
    retailer = Mixin.retailer + '-hk'
    market = 'HK'
    start_urls = [
        'http://www.hollisterco.com.hk/en_HK/guys-tops-hoodies-and-sweatshirts?icmp=ICT:BTS18:M:HP:H:K:x:HDSWT:SeptWk2']
    allowed_domains = ['hollisterco.com.hk', 'anf.scene7.com']


class MixinTW(Mixin):
    retailer = Mixin.retailer + '-tw'
    market = 'TW'
    start_urls = [
        'http://www.hollisterco.com.tw/en_TW/guys-tops-hoodies-and-sweatshirts?icmp=ICT:BTS18:M:HP:H:K:x:HDSWT:SeptWk2']
    allowed_domains = ['hollisterco.com.tw', 'anf.scene7.com']


class HollisterParseSpider(BaseParseSpider):
    care_css = '.product-sub-description.clearfix li::text'
    description_x = '//div[@class="product-sub-description"]/text()'
    price_css = ".product-price.clearfix"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender(garment)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.request_colors(response)}
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.request_images(response) + self.request_size(response)
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        requests = self.request_fiting(response)
        garment['meta']['requests_queue'] += requests

        if not requests:
            garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def parse_fiting(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment["image_urls"] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_id(response):
        return clean(response.css("#pid ::attr(value)"))[0]

    @staticmethod
    def product_name(response):
        return clean(response.css('.product-content .product-name ::text'))[0]

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb span::text'))

    def gender(self, garment):
        return self.gender_lookup(' '.join(garment['category'])) or Gender.ADULTS.value

    def request_colors(self, response):
        color_urls = clean(response.css('.swatches.color li span::attr(data-href)'))
        return [response.follow(add_or_replace_parameter(url, 'format', 'ajax'), self.parse_color) for url in
                color_urls]

    def request_size(self, response):
        size_urls = clean(response.css('.product__sizes .attribute:first-child span ::attr(data-href)'))
        return [response.follow(add_or_replace_parameter(url, 'format', 'ajax'), self.parse_size) for url in size_urls]

    def request_fiting(self, response):
        fiting_urls = clean(response.css('.product__sizes .attribute:nth-child(2) span ::attr(data-href)'))
        return [response.follow(add_or_replace_parameter(url, 'format', 'ajax'), self.parse_fiting) for url in
                fiting_urls]

    def request_images(self, response):
        url = clean(response.xpath("//input[@name='scene7url']/@value"))[0]
        return [response.follow(url, self.parse_images)]

    def image_urls(self, response):
        image_urls = []
        images = re.findall('scene7JSONResponse\((.*)\,"colorSet"\);', response.text)[0]
        images = json.loads(images)
        for image in images['set']['item'][0]['set']['item']:

            if image.get('i') is not None:
                image_urls.append(urljoin(self.image_api_url, image.get('i').get('n')))

        return image_urls

    def skus(self, response):
        sku = self.product_pricing_common(response)
        colour_xpath = '//input[@name="selectedcolor"]/@value'
        sku['colour'] = colour = clean(response.xpath(colour_xpath))[0]

        size_css = '.product__sizes .attribute:contains(Size) .selected ::attr(title)'
        size_fit = clean(response.css(size_css)) or [self.one_size][0]
        sku['size'] = size = size_fit[0]

        fit_css = '.product__sizes .attribute:contains(Fit) .selected ::attr(title)'
        sku['length'] = clean(response.css(fit_css)) or [''][0]

        sku_id = f'{colour}_{size}' if colour else f'{size}'
        return {sku_id: sku}


class HollisterCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '.category-navigation.secondary-nav-header .nav-link',
        '.Category .refinement-link',
        'infinite-scroll-placeholder'
    ]
    product_css = '.thumb-link'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=['a', 'div'], attrs=['href', 'data-grid-url'])
             ),
        Rule(
            LinkExtractor(restrict_css=product_css), callback='parse_item'
        )
    )


class HollisterJPParseSpider(MixinJP, HollisterParseSpider):
    name = MixinJP.retailer + '-parse'


class HollisterCNParseSpider(MixinCN, HollisterParseSpider):
    name = MixinCN.retailer + '-parse'


class HollisterHKParseSpider(MixinHK, HollisterParseSpider):
    name = MixinHK.retailer + '-parse'


class HollisterTWParseSpider(MixinTW, HollisterParseSpider):
    name = MixinTW.retailer + '-parse'


class HollisterJPCrawler(MixinJP, HollisterCrawlSpider):
    name = MixinJP.retailer + '-crawl'
    parse_spider = HollisterJPParseSpider()


class HollisterCNCrawler(MixinCN, HollisterCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = HollisterCNParseSpider()


class HollisterHKCrawler(MixinHK, HollisterCrawlSpider):
    name = MixinHK.retailer + '-crawl'
    parse_spider = HollisterHKParseSpider()


class HollisterTWCrawler(MixinTW, HollisterCrawlSpider):
    name = MixinTW.retailer + '-crawl'
    parse_spider = HollisterTWParseSpider()
