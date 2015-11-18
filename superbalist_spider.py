# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, CurrencyParser
from base import clean
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import json
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse


class Mixin(object):
    retailer = 'superbalist-za'
    allowed_domains = ['superbalist.com']
    market = 'ZA'
    start_urls_with_meta = [('http://superbalist.com/browse/women?page=1', {'gender': 'women'}),
                            ('http://superbalist.com/browse/men?page=1', {'gender': 'men'}),
                            ('http://superbalist.com/browse/apartment/decor?page=1', {'industry': 'homeware'}),
                            ('http://superbalist.com/browse/apartment/bedding-bath?page=1', {'industry': 'homeware'})]


class SuperbalistParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    price_x = "(//span[@class='price price-retail']/text())[2]  |  //span[@class='price jsSpanItemPrice']/text()"
    oos_url_t = 'http://superbalist.com/products/check_availability/%s'
    take_first = TakeFirst()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        garment = self.new_unique_garment(self.product_id(response.url))
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)
        previous_price, price, currency = self.product_pricing(hxs)

        garment['price'] = price
        garment['currency'] = self.product_currency(hxs)
        garment['spider_name'] = self.name
        garment['category'] = self.product_category(response.url)
        garment['image_urls'] = self.product_images(hxs)
        garment['gender'] = response.meta.get('gender')
        garment['industry'] = response.meta.get('industry')
        garment['skus'] = self.skus(hxs)
        garment['meta'] = {'requests_queue': self.oos_requests(garment)}

        return self.next_request_or_garment(garment)

    def parse_oos(self, response):
        garment = response.meta['garment']
        jsn = json.loads(response.body)
        garment['skus'][jsn['sku_id']]['out_of_stock'] = jsn['status'] == 'SOLD OUT'
        garment['skus'][jsn['sku_id']]['price'] = CurrencyParser.lowest_price(jsn['price'])
        return self.next_request_or_garment(garment)

    def skus(self, hxs):
        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)
        color = clean(hxs.select("//strong[text()='Colour']/following::div[1]/text()")) or ['']
        ids = json.loads(self.take_first(clean(hxs.select("//div[@class='jsProductAttributeWidget']/@data-tree"))))
        if not ids['children']:
            sku_ids = clean(hxs.select("//div[@class='jsProductAttributeWidget']/@data-sku_id"))
            sizes = [self.one_size]
        else:
            sku_ids = [x['sku_id'] for x in ids['children']['size']['options'].values()]
            sizes = [str(x['value']) for x in ids['children']['size']['options'].values()]

        for sku_id, size in zip(sku_ids, sizes):
            sku = {
                'currency': currency or self.product_currency(hxs),
                'size': size,
                'colour': self.take_first(color),
            }
            if previous_price:
                sku['previous_price'] = previous_price
            skus["%s" % sku_id] = sku

        return skus

    def oos_requests(self, garment):
        return [Request(url=self.oos_url_t % x, callback=self.parse_oos) for x in garment['skus'].keys()]

    def product_currency(self, hxs):
        return self.take_first(clean(hxs.select("//meta[@itemprop='priceCurrency']/@content")))

    def product_images(self, hxs):
        return clean(hxs.select('//div[@class="layout pdp-gallery carousel-y"]//img/@src'))

    def product_id(self, url):
        return clean(urlparse(url).path.split('/')[-1])

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='headline-tight']/text()")))

    def product_care(self, hxs):
        return clean(hxs.select("//strong[text()='Fabrication']/following::div[1]/text() "
                                "| //strong[text()='Material']/following::div[1]/text()"))

    def product_category(self, url):
        return urlparse(url).path.split('/')[1:-2] if isinstance(url, str) else None

    def product_description(self, hxs):
        return clean(hxs.select("//div[@itemprop='description']//text()"))

    def product_brand(self, hxs):
        return self.take_first(clean(hxs.select("//a[@itemprop='brand']/text()") or
                     hxs.select("//strong[text()='Brand']/following::div[1]/text()")))


class SuperbalistCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SuperbalistParseSpider()

    listings_x = [
        '//li[@class="paginate-next"]',
    ]

    products_x = [
        "//div[@class='layout bucket-list bucket-list-6']//a",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    )


