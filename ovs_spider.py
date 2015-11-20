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


class Mixin(object):
    retailer = 'ovs-it'
    allowed_domains = ['ovs.it']
    market = 'IT'
    start_urls_with_meta = [('http://www.ovs.it/', {}),
                            ('http://www.ovs.it/beauty/makeup', {'gender': 'women'}),
                            ('http://www.ovs.it/beauty/corpo-e-bagno', {'gender': 'women'}),
                            ('http://www.ovs.it/beauty/accessori', {'gender': 'women'}),
                            ('http://www.ovs.it/beauty/profumi/profumi-donna', {'gender': 'women'}),
                            ('http://www.ovs.it/beauty/profumi/profumi-uomo', {'gender': 'men'})]


class OVSParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    price_x = "//div[@class='product-price']//text()"
    oos_url_t = "http://www.ovs.it/on/demandware.store/Sites-ovs-italy-Site/it_IT/Product-Variation?%s%s&Quantity=1&format=ajax"
    images_url_t = "(//a[@class='thumbnail-link'])[position() > 1]/@href | (//img[@class='primary-image']/@src)[1]"
    gender = {'donna': 'women', 'uomo': 'men', 'ragazza-9-14-anni': 'girls', 'ragazzo-9-14-anni': 'boys',
              'bambina-2-8-anni': 'girls', 'bambino-2-8-anni': 'boys'}
    take_first = TakeFirst()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        garment = self.new_unique_garment(self.product_id(response.url))
        if garment is None:
            return

        self.boilerplate_normal(garment, hxs, response)
        previous_price, price, currency = self.product_pricing(hxs)

        garment['price'] = price
        garment['currency'] = currency
        garment['spider_name'] = self.name
        garment['category'] = self.product_category(garment)
        garment['lang'] = self.product_lang(hxs)
        garment['gender'] = response.meta.get('gender') or self.product_gender(garment)
        garment['outlet'] = self.product_outlet(garment)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.oos_requests(hxs)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)
        color = self.take_first(clean(hxs.select('(//li[@class="selected-value"])[1]/text()')))
        if color not in [x['colour'] for x in garment['skus'].values()]:
            garment['image_urls'] += clean(hxs.select(self.images_url_t))
        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)
        size = self.take_first(clean(hxs.select('(//li[@class="selected-value"])[2]/text()')))
        out_of_stock = bool(clean(hxs.select("//p[@class='non-in-stock-msg']/text()")))
        sku = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': color,
            'out_of_stock': out_of_stock
        }
        if previous_price:
            sku['previous_price'] = previous_price
        skus[color + '_' + size] = sku
        garment['skus'].update(skus)

        return self.next_request_or_garment(garment)

    def oos_requests(self, hxs):
        queue = []
        colors = clean(hxs.select("//ul[@class='swatches Color']//a/@href"))
        sizes = clean((hxs.select("//ul[@class='swatches size']//a/@href")))
        for color in colors:
            for size in sizes:
                queue += [Request(url=self.oos_url_t % (color.split('?')[-1], '&' + size.split('&')[-1])
                                  , callback=self.parse_skus)]
        return queue

    def product_images(self, hxs):
        return clean(hxs.select("//ul[@class='thumbnails_ul']//a/@href"))

    def product_id(self, url):
        return clean(urlparse(url).path.split('/')[-1].strip('.html'))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@class='product-name']//text()")))

    def product_care(self, hxs):
        return clean(hxs.select("//div[@itemprop='shortDescription']//text()"))

    def product_category(self, garment):
        return urlparse(garment['trail'][-1][1]).path.split('/')[1:] if isinstance(garment, Garment) else None

    def product_description(self, hxs):
        return clean(hxs.select("//div[@itemprop='description']//text()"))

    def product_brand(self, hxs):
        return "OVS"

    def product_lang(self, hxs):
        return self.take_first(clean(hxs.select('//ul[@class="menu-utility-style menu-utility'
                                                '-language"]//a[@class="active"]/text()')))

    def product_outlet(self, garment):
        return urlparse(garment['trail'][-1][1]).path.split('/')[1] == 'outlet'

    def product_gender(self, garment):
        key = urlparse(garment['trail'][-1][1]).path.split('/')[1:]
        return self.gender.get(key[0]) or self.gender.get(key[1]) or self.gender.get(key[-1]) or 'unisex-kids'


class OVSCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = OVSParseSpider()

    listings_x = [
        "(//li[@class='current-page'])[1]/following::li[1]//@href",
        '//a[text()="Collezione"]/following-sibling::div//a',
        '//li[@class="sellable  last"]//div[@class="level-3"]//a',
    ]

    products_x = [
        "//div[@class='search-result-content']//a[@class='thumb-link']",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item', process_request='process_request'),
    )

    def process_request(self, req):
        return req.replace(url=req.url.split('?')[0])





