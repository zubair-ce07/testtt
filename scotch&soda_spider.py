# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.http import Request, Response
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
    gender_map = {
        u'damen': u'women',
        u'herren': u'men',
        u'mädchen': u'girls',
        u'madchen': u'girls',
        u'jungen': u'boys',
    }


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
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['category'] = self.product_category(response)
        if 'living' in [x.lower() for x in garment['category']]:
            garment['industry'] = 'homeware'
        else:
            gender = garment['category'][0].replace(u'\xe4', u'a').lower()
            garment['gender'] = self.gender_map.get(gender, '') if hasattr(self, 'gender_map') else gender

        garment['brand'] = self.product_brand(garment['category'][0].lower())
        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.skus_requests(hxs)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)

        sku_color = url_query_parameter(response.url, 'dwvar_' + url_query_parameter(response.url, 'pid') + '_color')
        parsed_colors = [x.get('color') for x in garment['skus'].itervalues()]
        if sku_color not in parsed_colors:
            garment['image_urls'] += self.image_urls(hxs)

        garment['skus'].update(self.skus(hxs, response.url))

        return self.next_request_or_garment(garment)

    def skus_requests(self, hxs):
        colors = clean(hxs.select("//ul[@id='js-swatches']/li/a/@href"))
        sizes = clean(hxs.select("//ul[@class='swatches size product-property__list product-property--sizes"
                                 "__list js-collapsible--pdp']/li/a/text()"))
        requests = []
        sku_url_t = '%s&dwvar_' + self.product_id(hxs) + '_size=%s&format=ajax&Quantity=1'
        for color in colors:
            for size in sizes:
                sku_url = sku_url_t % (color, size)
                requests.append(Request(sku_url, callback=self.parse_skus))

        return requests

    def skus(self, hxs, url):
        skus = {}
        previous_price, price, currency = self.product_pricing(hxs)

        pid = 'dwvar_' + url_query_parameter(url, 'pid')
        color = url_query_parameter(url, pid + '_color')
        size = url_query_parameter(url, pid + '_size')

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
        if not isinstance(response, Response):
            return

        xpath = "//div[contains(@class,'breadcrumbs')]//li//text()"
        # The or part is for a rare case when breadcrumbs are empty
        return clean(HtmlXPathSelector(response).select(xpath))[1:] or\
               urlparse(response.url).path.split('/')[4:-2]

    def product_brand(self, category):
        category = unicode(category)
        return self.brand_map.get(category) if isinstance(category, unicode) else None

    def raw_description(self, hxs):
        return clean(hxs.select("//span[@class='fabric']//li/text() |"
                                " //div[@class='product-short-description']/text()"))

    def product_description(self, hxs):
        raw_desc = self.raw_description(hxs)
        return [x for x in raw_desc if not self.care_criteria(x)]

    def product_care(self, hxs):
        care = clean(hxs.select("//span[starts-with(text(), 'What it') or"
                                " starts-with(text(), 'Woraus der Artikel')]/text()"))
        raw_desc = self.raw_description(hxs)
        return care + [x for x in raw_desc if self.care_criteria(x)]


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
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, process_value=lambda r: url_query_cleaner(r)),
             callback='parse_item'),
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
