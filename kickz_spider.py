# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, CurrencyParser
from base import clean, tokenize
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from skuscraper.items import Garment
import re
from operator import itemgetter
from itertools import groupby


class Mixin(object):
    retailer = 'kickz-de'
    allowed_domains = ['www.kickz.com', 'kickz.akamaized.net']
    market = 'DE'
    lang = 'de'
    start_urls_with_meta = [('https://www.kickz.com/de/support/static/homepage-men', {'gender': 'men'}),
                            ('https://www.kickz.com/de/support/static/homepage-women', {'gender': 'women'}),
                            ('https://www.kickz.com/de/support/static/homepage-kids', {'gender': 'unisex-kids'}),
                            ('https://www.kickz.com/de/Kids/accessoires,Stuff/c', {'gender': 'unisex-kids'}),
                            ('https://www.kickz.com/de/Maenner/accessoires,Stuff/c', {'gender': 'men'}),
                            ('https://www.kickz.com/de/Frauen/accessoires,Stuff/c', {'gender': 'women'})]


class KickzParseSpider(BaseParseSpider, Mixin):

    handle_httpstatus_list = [404]
    name = Mixin.retailer + '-parse'
    sku_url_t = "https://www.kickz.com/de/%s"
    price_x = "//span[@class='currentPriceId']//text() |  //span[@id='oldPriceId']/text()"
    coming_soon_x = "//div[@id='counter_header']"
    take_first = TakeFirst()
    unwanted_categories = {
        u'energy',
        u'drinks',
        u'gutscheine',
        u'schuhpflege',
        u'b\xfccher',
        u'magazine'
        u'handtücher',
        u'schnürsenkel',
    }

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if garment is None:
            return

        tokens = tokenize(self.product_category(hxs))
        if tokens & self.unwanted_categories:
            self.log('Drop unwanted item at %s' % response.url)
            return

        self.boilerplate(garment, hxs, response)
        garment['name'] = self.product_name(hxs)
        garment['category'] = self.product_category(hxs)
        garment['brand'] = self.product_brand(garment)
        garment['care'] = self.product_care(hxs)
        garment['gender'] = self.product_gender((self.product_name(hxs)).lower()) or response.meta.get('gender')
        if self.out_of_stock(hxs):
            return self.out_of_stock_garment(response, pid)
        else:
            garment['skus'] = self.skus(response)
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.sku_requests(hxs) + self.image_urls(hxs)}
        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)
        garment['meta']['requests_queue'] += self.image_urls(hxs)
        if self.out_of_stock(hxs):
            garment['skus'].update({self.product_id(hxs): {'out_of_stock': True}})
        else:
            garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        if response.status != 404 and response.url not in garment['image_urls']:
            garment['image_urls'] += [response.url]
        else:
            for _ in range(6-int(re.search('(\d).jpg', response.url).group(1))):
                garment['meta']['requests_queue'].pop()

        return self.next_request_or_garment(garment)

    def out_of_stock(self, hxs):
        return bool(hxs.select("//span[@class='priceOfftxt'][starts-with(text(),'Leider ausverkauft')]"))

    def image_urls(self, hxs):
        image_urls = clean(hxs.select("//ul[@id='thumblist']//img[not(@style='display: none;')]/@data-zoom-img"))
        return list(reversed([Request(url=x, callback=self.parse_image_urls, dont_filter=True) for x in image_urls]))

    def skus(self, response):
        hxs = HtmlXPathSelector(response)
        skus = {}
        color = self.take_first(clean(hxs.select("//span[@id='variantColorId']//text()")))
        skus_data = [x.re("'(.*)'") for x in hxs.select("//div[@id='1SizeContainer']//a/@onclick")]

        for sku_data in skus_data:

            sku = {
                'price': CurrencyParser.lowest_price(sku_data[2]),
                'currency': CurrencyParser.currency(sku_data[2]),
                'size': self.one_size if sku_data[5] == 'one' else sku_data[5],
                'colour': color,
                'out_of_stock': bool(clean(hxs.select(self.coming_soon_x))),
                'previous_prices': [CurrencyParser.lowest_price([sku_data[1]][0])]
            }
            if self.take_first(sku['previous_prices']) == sku['price']:
                    sku.pop('previous_prices')
            skus[sku_data[0]] = sku
        return skus

    def sku_requests(self, hxs):
        colors = clean(hxs.select("//a[@class='chooseColorLink']/@href"))
        return [Request(url=self.sku_url_t % color, callback=self.parse_skus) for color in colors]

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//input[@name='productErp']/@value"))
                               or clean(hxs.select("//span[@itemprop='productID']/text()")))

    def product_gender(self, name):
        if ('boy' or 'boys') in name:
            return 'boys'
        if ('girls' or 'girl') in name:
            return 'girls'

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@id='prodNameId']/text()")))

    def product_care(self, hxs):
        return clean(hxs.select("//b[text()='Material:']/ancestor::div[1]/text()"))

    def product_category(self, hxs):
        category = clean([x.strip('>') for x in clean(hxs.select("//div[@class='breadcrumb_catalog']//text()"))[1:-2]])
        return list(map(itemgetter(0), groupby(category)))

    def product_brand(self, garment):
        return garment['category'][-1] if isinstance(garment, Garment) else None


class KickzCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = KickzParseSpider()
    listings_x = [
        "//a[@class='pagerBox pagerBoxRight']",
        "(//li[starts-with(@id,'sub_menu_list')]/a)[position() < 3]",
    ]
    products_x = [
        "//div[@id='product_list_container']/div/a",
    ]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    )
