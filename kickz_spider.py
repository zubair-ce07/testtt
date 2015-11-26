# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, CurrencyParser
from base import clean, tokenize
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst
from skuscraper.items import Garment


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
    take_first = TakeFirst()
    unwanted_tokens = {
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
        garment = self.new_unique_garment(self.product_id(hxs))
        if garment is None:
            return

        tokens = tokenize(self.product_category(hxs))
        if tokens & self.unwanted_tokens:
            self.log('Dropped unwanted item')
            return

        self.boilerplate_normal(garment, hxs, response)
        garment['category'] = self.product_category(hxs)
        garment['brand'] = self.product_brand(garment)
        garment['gender'] = response.meta.get('gender')
        garment['skus'] = self.skus(response)
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.sku_requests(hxs) + self.image_urls(hxs)}
        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        hxs = HtmlXPathSelector(response)
        garment['meta']['requests_queue'] += self.image_urls(hxs)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        if response.status != 404:
            garment['image_urls'] += [response.url]
        return self.next_request_or_garment(garment)

    def image_urls(self, hxs):
        image_urls = clean(hxs.select("//ul[@id='thumblist']//img[not(@style='display: none;')]/@data-zoom-img"))
        return [Request(url=x, callback=self.parse_image_urls) for x in image_urls]

    def skus(self, response):
        hxs = HtmlXPathSelector(response)
        skus = {}
        color = self.take_first(clean(hxs.select("//span[@id='variantColorId']//text()")))
        skus_data = clean(hxs.select("//div[@class='chooseSizeContainer'][1]/div/a/@onclick"))
        skus_data = [x.strip("ProductDetails.changeSizeAffectedLinks( '").strip("');").split("', '") for x in skus_data]

        for sku_data in skus_data:
            sku = {
                'price': CurrencyParser.lowest_price(sku_data[2]),
                'currency': CurrencyParser.currency(sku_data[2]),
                'size': sku_data[5],
                'colour': color,
                'out_of_stock': not clean(sku_data[8]),
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
        return self.take_first(clean(hxs.select("//span[@itemprop='productID']/text()")))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@id='prodNameId']/text()")))

    def product_care(self, hxs):
        return clean(hxs.select("//b[text()='Material:']/ancestor::div[1]/text()"))

    def product_category(self, hxs):
        return clean([x.strip('>') for x in clean(hxs.select("//div[@class='breadcrumb_catalog']//text()"))[:-2]])

    def product_description(self, hxs):
        return clean(hxs.select("//h2[starts-with(text(),'Markeninfo')]/preceding-sibling::"
                                "div[@class='details_text']//text()[not(ancestor::style)]"))

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
        "//div[@class='categoryElementSpecial']/following::a[1]",
    ]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    )