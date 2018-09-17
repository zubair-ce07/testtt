import json
import re
from urllib.parse import urljoin

from scrapy import Request
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
        'http://www.hollisterco.jp/en_JP/guys-tops-hoodies-and-sweatshirts?icmp=ICT:BTS18:M:HP:H:K:x:HDSWT:SeptWk2']
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


class GenericParser(BaseParseSpider):
    care_css = '.product-sub-description.clearfix li::text'
    description_x = '//div[@class="product-sub-description"]/text()'
    price_css = ".product-price.clearfix"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender(garment['category'])
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.request_colors(response)}
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_id(response):
        return clean(response.css(".find-in-store ::attr(pid)"))[0]

    @staticmethod
    def product_name(response):
        return clean(response.css('.product-content .product-name ::text'))[0]

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb span::text'))

    def gender(self, category):
        return self.gender_lookup(' '.join(category)) or Gender.ADULTS.value

    def request_colors(self, response):
        requests = []
        color_urls = clean(response.css('.swatches.color li span::attr(data-href)'))
        for url in color_urls:
            url = add_or_replace_parameter(url, 'format', 'ajax')
            requests.append(Request(url=url, callback=self.parse_color))
        return requests

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += (self.request_images(response) + self.request_size(response))
        return self.next_request_or_garment(garment)

    def request_size(self, response):
        requests = []
        size_sel = response.css('.swatches.option')
        size_urls = clean(size_sel[0].css('.swatchanchor ::attr(data-href)'))
        for url in size_urls:
            url = add_or_replace_parameter(url, 'format', 'ajax')
            requests.append(Request(url=url, callback=self.parse_size))
        return requests

    def parse_size(self, response):
        garment = response.meta['garment']
        requests = self.request_fiting(response)
        garment['meta']['requests_queue'] += requests
        if not requests:
            garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def request_fiting(self, response):
        requests = []
        fiting_sel = response.css('.swatches.option')
        if len(fiting_sel) > 1:
            fiting_urls = clean(fiting_sel[1].css('.swatchanchor ::attr(data-href)'))
            for url in fiting_urls:
                url = add_or_replace_parameter(url, 'format', 'ajax')
                requests.append(Request(url=url, callback=self.parse_fiting))
            return requests
        return []

    def parse_fiting(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def request_images(self, response):
        url = clean(response.xpath("//input[@name='scene7url']/@value"))[0]
        return [Request(url=url, callback=self.parse_images)]

    def parse_images(self, response):
        garment = response.meta['garment']
        garment["image_urls"] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def image_urls(self, response):
        images = []
        json_data = re.findall('scene7JSONResponse\((.*)\,"colorSet"\);', response.text)[0]
        image_urls = json.loads(json_data)
        for image in image_urls['set']['item']['set']['item']:
            images.append(urljoin(self.image_api_url, image.get('i', {}).get('n')))
        return images

    def skus(self, response):
        colour_xpath = '//input[@name="selectedcolor"]/@value'
        size_fit_xpath = '.product__sizes .selected::attr(title)'
        sku = self.product_pricing_common(response)
        size_fit = clean(response.css(size_fit_xpath)) or [self.one_size]
        sku['colour'] = colour = clean(response.xpath(colour_xpath))[0]
        if len(size_fit) > 1:
            sku['size'] = size = size_fit[0]
            sku['length'] = size_fit[1]
        else:
            sku['size'] = size = size_fit[0]
            fit_sel = response.css('.swatches.option')
            if len(fit_sel) > 1:
                sku['length'] = clean(fit_sel[1].css('.list-item ::attr(title)'))[0]
        sku_id = f'{colour}_{size}' if colour else f'{size}'
        return {sku_id: sku}


class GenericCrawler(BaseCrawlSpider):
    listing_css = [
        '.category-navigation.secondary-nav-header .nav-link',
        '.Category .refinement-link',
        'infinite-scroll-placeholder'
    ]
    productCard_css = '.thumb-link'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=['a', 'div'], attrs=['href', 'data-grid-url'])
             ),
        Rule(
            LinkExtractor(restrict_css=productCard_css), callback='parse_item'
        )
    )


class HollisterJPParseSpider(MixinJP, GenericParser):
    name = MixinJP.retailer + '-parse'


class HollisterCNParseSpider(MixinCN, GenericParser):
    name = MixinCN.retailer + '-parse'


class HollisterHKParseSpider(MixinHK, GenericParser):
    name = MixinHK.retailer + '-parse'


class HollisterTWParseSpider(MixinTW, GenericParser):
    name = MixinTW.retailer + '-parse'


class HollisterJPCrawler(MixinJP, GenericCrawler):
    name = MixinJP.retailer + '-crawl'
    parse_spider = HollisterJPParseSpider()


class HollisterCNCrawler(MixinCN, GenericCrawler):
    name = MixinCN.retailer + '-crawl'
    parse_spider = HollisterCNParseSpider()


class HollisterHKCrawler(MixinHK, GenericCrawler):
    name = MixinHK.retailer + '-crawl'
    parse_spider = HollisterHKParseSpider()


class HollisterTWCrawler(MixinTW, GenericCrawler):
    name = MixinTW.retailer + '-crawl'
    parse_spider = HollisterTWParseSpider()
