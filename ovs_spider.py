# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from skuscraper.items import Garment
from scrapy.utils.url import url_query_cleaner as uqc, url_query_parameter as uqp


class Mixin(object):
    retailer = 'ovs-it'
    allowed_domains = ['www.ovs.it']
    market = 'IT'
    lang = 'it'
    start_urls = ['http://www.ovs.it/']


class OVSParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    price_x = "//div[@class='product-price']//text()"
    sku_url_t = "http://www.ovs.it/on/demandware.store/Sites-ovs-italy-Site/it_IT/Product-Variation?%s%s&Quantity=1" \
                "&format=ajax"
    size_x = '//a[contains(@href,"%s")]/@title'
    images_url_x = "(//a[@class='thumbnail-link'])[position() > 1]/@href | (//img[@class='primary-image']/@src)[1]"
    gender = {'donna': 'women', 'uomo': 'men', 'ragazza-9-14-anni': 'girls', 'ragazzo-9-14-anni': 'boys',
              'bambina-2-8-anni': 'girls', 'bambino-2-8-anni': 'boys', 'beauty': 'women', 'profumi-donna': 'women',
              'profumi-uomo': 'men'}
    take_first = TakeFirst()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        garment = self.new_unique_garment(self.product_id(response.url))
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['category'] = self.product_category(garment)
        garment['gender'] = self.product_gender(garment)
        garment['outlet'] = self.product_outlet(garment)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.sku_requests(hxs)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)
        garment['image_urls'] += [uqc(x) for x in self.image_urls(hxs, [x['colour'] for x in garment['skus'].values()])]
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def image_urls(self, hxs, colors):
        color = self.take_first(clean(hxs.select('(//li[@class="selected-value"])[1]/text()')))
        return clean(hxs.select(self.images_url_x)) if color not in colors else []

    def skus(self, response):
        hxs = HtmlXPathSelector(response)
        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)
        color = self.take_first(clean(hxs.select('(//li[@class="selected-value"])[1]/text()')))
        size = self.take_first(clean(hxs.select('(//li[@class="selected-value"])[2]/text()')) or
                               clean(hxs.select(self.size_x % uqp(response.url, 'dwvar_' + uqp(response.url, 'pid') +
                                                                  '_size'))))
        out_of_stock = not bool(clean(hxs.select("//p[@class='in-stock-msg']/text()")))
        sku = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': color,
            'out_of_stock': out_of_stock
        }
        if previous_price:
            sku['previous_prices'] = [previous_price]
        skus[color + '_' + size] = sku
        return skus

    def sku_requests(self, hxs):
        requests = []
        colors = clean(hxs.select("//ul[@class='swatches Color']//a/@href"))
        sizes = clean((hxs.select("//ul[@class='swatches size']//a/@href")))
        for color in colors:
            for size in sizes:
                requests += [Request(url=self.sku_url_t % (color.split('?')[-1], '&' + size.split('&')[-1]),
                                     callback=self.parse_skus)]
        return requests

    def product_id(self, url):
        return clean(urlparse(url).path.split('/')[-1].strip('.html'))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='product-name']//text()")))

    def product_care(self, hxs):
        return clean(hxs.select("//div[@itemprop='shortDescription']//text() |"
                                " //div[@id='containerDrySymbolsDefault']//div[not(@title='null')]/@title"))

    def product_category(self, garment):
        return urlparse(garment['trail'][-1][1]).path.split('/')[1:] if isinstance(garment, Garment) else None

    def product_description(self, hxs):
        return clean(hxs.select("//div[@itemprop='description']//text()"))

    def product_brand(self, hxs):
        return "OVS"

    def product_outlet(self, garment):
        return 'outlet' in garment['category']

    def product_gender(self, garment):
        key = garment['category']
        return self.gender.get(key[-1]) or self.gender.get(key[0]) or self.gender.get(key[1]) or 'unisex-kids'


class OVSCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = OVSParseSpider()
    listings_x = [
        "(//li[@class='current-page'])[1]/following::li[1]",
        "//a[text()='Collezione']/following-sibling::div//a",
        "//li[@class='sellable  last']//div[@class='level-3']//a",
        "//div[text()='Beauty']/following::li[not(@class='last')][position() < 6]",
    ]
    products_x = [
        "//div[@class='search-result-content']//a[@class='thumb-link']",
    ]
    deny_urls = ('ovs-for-expo', 'html', 'ovs-app-community', 'studentlovsshopping')
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=deny_urls), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, process_value=lambda r: uqc(r)), callback='parse_item'),
    )