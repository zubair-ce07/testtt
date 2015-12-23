# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, clean, tokenize, reset_cookies
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
import re
import json


class Mixin(object):
    retailer = 'thekooples-fr'
    market = 'FR'
    allowed_domains = ['thekooples.com']
    start_urls = ['http://www.thekooples.com/fr/']
    lang = 'fr'


class TheKooplesParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'
    take_first = TakeFirst()
    price_x = "//div[@class='price-info']//text()"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        if 'enfant' in tokenize(self.product_name(hxs)):
            response.meta['gender'] = 'unisex-kids'

        self.boilerplate_normal(garment, hxs, response)

        garment['category'] = self.product_category(response.url)
        garment['skus'] = self.skus(hxs)
        garment['image_urls'] = self.image_urls(hxs)
        garment['meta'] = {'requests_queue': self.sku_requests(hxs)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        if 'no-route' in response.url:
            return self.next_request_or_garment(garment)

        hxs = HtmlXPathSelector(response)

        garment['image_urls'] += self.image_urls(hxs)
        garment['skus'].update(self.skus(hxs))

        return self.next_request_or_garment(garment)

    def sku_requests(self, hxs):
        color_urls = clean(hxs.select("//figure[@class='product-colors-image']//a[@class!='current-product']/@href"))
        return [Request(url=color_url, callback=self.parse_skus) for color_url in color_urls]

    def skus(self, hxs):
        skus = {}
        json_data = self.take_first(clean(hxs.select("//script[contains(text(), 'new Product.Config(')]//text()")))
        json_data = json.loads(re.findall('Product.Config\(({.*})', json_data)[0])
        color = self.take_first(clean(hxs.select("//*[@class='current-product']//img/@title"))).title()

        previous_price, price, currency = self.product_pricing(hxs)

        for product_data in json_data['attributes']['257']['options']:
            size = product_data['label']
            sku = {
                'price': price,
                'currency': currency,
                'size': size if size != 'TU' else self.one_size,
                'colour': color,
                'out_of_stock': product_data['dataStock'] != '1',
            }

            if previous_price:
                sku['previous_prices'] = [previous_price]

            sku_id = self.take_first(product_data['productId'])
            skus[sku_id] = sku

        return skus

    def image_urls(self, hxs):
        return clean(hxs.select("//img[@class='gallery-image']/@src"))

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//p[@class='product-ref']/text()").re('Ref : ([A-Z]*[0-9]*)')))

    def product_category(self, url):
        return urlparse(url).path.split('/')[2:-1] if isinstance(url, str) else None

    def product_name(self, hxs):
        # There are few items with empty title
        return (clean(hxs.select("//h1[@class='product-page-title']//text()")) or [''])[0]

    def product_brand(self, hxs):
        if self.take_first(clean(hxs.select("//input[@id='is_sport_collection']/@value"))) == '1':
            return 'The Kooples Sport'

        return 'The Kooples'

    def product_care(self, hxs):
        return clean(hxs.select("//div[@id='block-composition']//p//text() |"
                                " //div[@id='block-care']//li/i/@title"))

    def product_description(self, hxs):
        return clean(hxs.select("//div[@id='block-description']//p[1]/text()"))


class TheKooplesCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = TheKooplesParseSpider()

    section_x_t = "//ul[@class='level0']/parent::li[contains(@data-code,'%s')]//ul"
    men_x = section_x_t % '-MEN'
    women_x = section_x_t % 'WOMEN'

    products_x = '//ul[@id="products-grid-sort"]'

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=men_x,  process_value=lambda x: x.replace('&ajax=1', '')),
             process_request=reset_cookies, callback='parse_and_add_men'),

        Rule(SgmlLinkExtractor(restrict_xpaths=women_x, process_value=lambda x: x.replace('&ajax=1', '')),
             process_request=reset_cookies, callback='parse_and_add_women'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x),
             process_request=reset_cookies, callback='parse_item')
    )
