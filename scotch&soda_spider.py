# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.http import Request
from scrapy.utils.url import url_query_parameter, url_query_cleaner
from urlparse import urlparse


class Mixin(object):
    retailer = 'scotchandsoda'
    allowed_domains = ['www.scotch-soda.com']
    pfx = 'https://www.scotch-soda.com/'


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = [Mixin.pfx + 'gb/en/home']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    market = 'DE'
    start_urls = [Mixin.pfx + 'de/de/home']


class ScotchandSodaParseSpider(BaseParseSpider):

    price_x = "//span[@class='product-price']//text()"
    take_first = TakeFirst()
    brand_map = {
        u'women': u'Maison Scotch',
        u'damen': u'Maison Scotch',
        u'men': u'Scotch & Soda',
        u'herren': u'Scotch & Soda',
        u'girls': u"Scotch R'Belle",
        u'mädchen': u"Scotch R'Belle",
        u'madchen': u"Scotch R'Belle",
        u'boys': u'Scotch Shrunk',
        u'jungen': u'Scotch Shrunk',
        u'living': u'Scotch & Soda',
    }

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if garment is None:
            return
        self.boilerplate_normal(garment, hxs, response)
        garment['category'] = self.product_category(response)
        if 'living' in [x.lower() for x in garment['category']]:
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = garment['category'][0]
        garment['brand'] = self.product_brand(garment['category'][0].lower())
        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.skus_requests(hxs)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)
        if url_query_parameter(response.url, 'dwvar_' + url_query_parameter(response.url, 'pid') + '_color') not in \
                [x.get('color') for x in garment['skus'].itervalues()]:
            garment['image_urls'] += self.image_urls(hxs)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def skus_requests(self, hxs):
        colors = clean(hxs.select("//ul[@id='js-swatches']/li/a/@href"))
        sizes = clean(hxs.select("//ul[@class='swatches size product-property__list product-property--sizes"
                                 "__list js-collapsible--pdp']/li/a/text()"))
        for color in colors:
            for size in sizes:
                yield Request(url=color + '&dwvar_' + self.product_id(hxs) + '_size=' + size +
                                   '&format=ajax&Quantity=1',callback=self.parse_skus)

    def skus(self, response):
        hxs = HtmlXPathSelector(response)
        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)
        color = url_query_parameter(response.url, 'dwvar_' + url_query_parameter(response.url, 'pid') + '_color')
        size = url_query_parameter(response.url, 'dwvar_' + url_query_parameter(response.url, 'pid') + '_size')
        size = self.one_size if size == 'OS' or (not size) else size
        sku = {
            'price': price,
            'currency': currency,
            'size': size,
            'color': color,
            'out_of_stock': bool(hxs.select("//span[@class='out-of-stock']")),
        }
        if previous_price:
            sku['previous_prices'] = [previous_price]
        skus[color + '_' + size if color else size] = sku
        return skus

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//span[@class='article-number']/text()"))).split(': ')[1]

    def image_urls(self, hxs):
        return clean(hxs.select("(//ul[@id='js-pdp-carousel'])[1]//a/@href"))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h2[@class='product-name']/text()")))

    def product_category(self, response):
        if not isinstance(response, HtmlXPathSelector):
            return clean(HtmlXPathSelector(response).select("//div[@class='grid__unit s-1-1 breadcrumbs']//li//text()")
                        )[1:] or urlparse(response.url).path.split('/')[4:-2]

    def product_brand(self, category):
        category = unicode(category)
        return self.brand_map.get(category) if isinstance(category, unicode) else None

    def raw_description(self, hxs):
        return clean(hxs.select("//span[@class='fabric']//li/text()"))

    def product_description(self, hxs):
        raw_desc = self.raw_description(hxs)
        return [x for x in raw_desc if not self.care_criteria_simplified(x)]

    def product_care(self, hxs):
        care1 = clean(hxs.select("//span[starts-with(text(), 'What it') or"
                                " starts-with(text(), 'Woraus der Artikel')]/text()"))
        care2 = self.raw_description(hxs)
        return care1 + [x for x in care2 if self.care_criteria_simplified(x)]


class ScotchandSodaCrawlSpider(BaseCrawlSpider, Mixin):

    listings_x = [
        "//li[@class='pagination__item pagination__item--next']/a",
        "//b[@class='nav-dropdown__h'][contains(text(), 'Categories') or contains(text(), 'Kategorien')]"
        "/parent::div//ul",
    ]
    products_x = [
        "//ul[@id='js-search-result-items']//a",
    ]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, process_value=lambda r: url_query_cleaner(r)), callback='parse_item'),
    )


class ScotchandSodaUKParseSpider(ScotchandSodaParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class ScotchandSodaUKCrawlSpider(ScotchandSodaCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ScotchandSodaUKParseSpider()


class ScotchandSodaDEParseSpider(ScotchandSodaParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class ScotchandSodaDECrawlSpider(ScotchandSodaCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = ScotchandSodaDEParseSpider()


