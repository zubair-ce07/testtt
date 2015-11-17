# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
import logging
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import json
from scrapy.contrib.spiders import Rule
from scrapy.http import Request


logging.basicConfig(level=logging.DEBUG,
                    format='(%(processName)-10s) %(message)s',  #: Output the Process Name just for checking purposes
                    )


class Mixin(object):
    retailer = 'superbalist'
    allowed_domains = ['superbalist.com']
    pfx = ['http://superbalist.com/browse?page=1']


class MixinZA(Mixin):
    retailer = Mixin.retailer + '-za'
    market = 'ZA'
    start_urls = Mixin.pfx


class SuperbalistParseSpider(BaseParseSpider):

    #: Path of money string
    price_x = "(//span[@class='price price-retail']/text())[2]  |  //span[@class='price jsSpanItemPrice']/text()"

    #: Callback function
    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        #: Initialize the garment object by giving it a unique id
        garment = self.new_unique_garment(self.product_id(response.url))
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)
        previous_price, price, currency = self.product_pricing(hxs)

        #: Setting parameters for a garment
        garment['price'] = price
        garment['currency'] = self.product_currency(hxs)
        garment['spider_name'] = self.name
        garment['image_urls'] = self.product_images(hxs)
        garment['gender'] = self.product_gender(response.url.split('/')[3])
        garment['skus'], queue = self.skus(hxs)
        garment['meta'] = {'requests_queue': queue}

        return self.next_request_or_garment(garment)

    def parse_oos(self, response):
        garment = response.meta['garment']
        jsn = json.loads(response.body)
        garment['skus'][response.url.split('/')[-1]]['out_of_stock'] = jsn['status'] == 'SOLD OUT'
        garment['skus'][response.url.split('/')[-1]]['price'] = jsn['price']
        return self.next_request_or_garment(garment)

    def skus(self, hxs):
        oos_url = 'http://superbalist.com/products/check_availability/%s'

        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)
        color = clean(hxs.select("//strong[text()='Colour']/following::div[1]/text()")) or ['']
        ids = json.loads(clean(hxs.select("//div[@class='jsProductAttributeWidget']/@data-tree"))[0])
        #: If there is no children
        if not ids['children']:
            sku_ids = clean(hxs.select("//div[@class='jsProductAttributeWidget']/@data-sku_id"))
            sizes = [self.one_size]
        else:
            sku_ids = map(lambda x: str(x['sku_id']), ids['children']['size']['options'].values())
            sizes = map(lambda x: str(x['value']), ids['children']['size']['options'].values())
        # Requests for checking oos
        queue = map(lambda x: Request(url=oos_url % x, callback=self.parse_oos), sku_ids)

        for sku_id, size in zip(sku_ids, sizes):
            sku = {
                'currency': currency or self.product_currency(hxs),
                'size': size,
                'colour': color[0],
            }
            if previous_price:
                sku['previous_price'] = previous_price
            skus[sku_id] = sku

        return skus, queue

    def product_currency(self, hxs):
        #: If base.py can't detect currency
        return clean(hxs.select("//meta[@itemprop='priceCurrency']/@content"))[0]

    def product_images(self, hxs):
        return clean(hxs.select('//div[@class="layout pdp-gallery carousel-y"]//img/@src'))

    def product_id(self, url):
        return url.split('/')[-1]

    def product_name(self, hxs):
        return clean(hxs.select("//h1[@class='headline-tight']/text()"))[0]

    def product_gender(self, value):
        return value if value in ['women', 'men'] else None

    def product_care(self, hxs):
        return clean(hxs.select("//strong[text()='Fabrication']/following::div[1]/text() "
                                "| //strong[text()='Material']/following::div[1]/text()"))

    def product_category(self, hxs):
        return clean(hxs.select("//li[@class='nav-breadcrumb-item']/a/text()"))

    def product_description(self, hxs):
        return clean(hxs.select("//div[@itemprop='description']//text()"))

    def product_brand(self, hxs):
        return clean(hxs.select("//a[@itemprop='brand']/text()")[0] or
                     hxs.select("//strong[text()='Brand']/following::div[1]/text()")[0])


class SuperbalistCrawlSpider(BaseCrawlSpider, Mixin):
    #: Set the rules for scraping all the available products of a website
    rules = (

        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                '//li[@class="paginate-next"]')),
            callback='parse', follow=True
        ),
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//div[@class='layout bucket-list bucket-list-6']//a")),
            callback='parse_item'
        ),
    )


class SuperbalistZAParseSpider(SuperbalistParseSpider, MixinZA):
    name = MixinZA.retailer + '-parse'


class SuperbalistZACrawlSpider(SuperbalistCrawlSpider, MixinZA):
    name = MixinZA.retailer + '-crawl'
    parse_spider = SuperbalistZAParseSpider()


