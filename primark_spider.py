# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, CurrencyParser
from base import clean, tokenize
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
import json
import re
from scrapy.http import Request


class Mixin(object):
    retailer = 'primark-uk'
    allowed_domains = ['www.primark.com', 'images.primark.com']
    market = 'UK'
    start_urls = ['http://www.primark.com/admin/productsapi/search//kids/1/500/Latest/true/en',
                  'http://www.primark.com/admin/productsapi/search//home/1/500/Latest/true/en',
                  'http://www.primark.com/admin/productsapi/search//women/1/500/Latest/true/en',
                  'http://www.primark.com/admin/productsapi/search//men/1/500/Latest/true/en',
                  'http://www.primark.com/admin/productsapi/search//beauty/1/500/Latest/true/en',
                  'http://www.primark.com/admin/productsapi/search//undefined/1/500/Latest/true/en',
                  ]

MAX_RETRIES = 3


class PrimarkParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//p[@id='price-value']//meta/@content"
    name_x = "(//div[@class='og-details'])[1]//div[@class='cell']/h3/text()"
    take_first = TakeFirst()
    gender_map = (
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('women', 'women'),
        ('men', 'men'),
        ('kid', 'unisex-kids'),
        ('beauty', 'women'),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        #: Re issue Request if data of the product is not loaded correctly
        if not self.product_name(hxs):
            return self.retry_request(response)

        pid = self.product_id(response.url)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        category = ' '.join(self.product_category(hxs))
        if 'home' in category:
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(category)

        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs, response.url)

        return garment

    def skus(self, hxs, url):
        skus = {}
        currency, price = CurrencyParser.currency_and_price(' '.join(clean(hxs.select(self.price_x))))

        color = " ".join(clean(self.detect_colour(x) for x in tokenize(self.product_name(hxs))))
        sku = {
            'price': price,
            'currency': currency,
        }
        if color:
            sku['color'] = color

        sku_id = self.take_first(clean(hxs.select("//p[@class='id-number']/span[starts-with(text(),'S')]/text()")))
        skus[sku_id if sku_id else self.product_id(url)] = sku

        return skus

    def product_id(self, url):
        return urlparse(url).path.split(',')[-1]

    def product_brand(self, hxs):
        return "Primark"

    def image_urls(self, hxs):
        return clean(hxs.select("(//div[@class='og-fullimg'])[1]//img/@src"))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select(self.name_x)))

    def product_category(self, hxs):
        return self.take_first(clean(hxs.select("//p[@class='category-link']//a/@href"))).split('/')[-1].split(',')

    def product_gender(self, category):
        for x, y in self.gender_map:
            if x in category:
                return y
        return 'unisex-kids'

    def product_description(self, hxs):
        return clean(hxs.select("//p[@class='description']/text()"))

    def product_care(self, hxs):
        return None

    def retry_request(self, response):
        retries = response.meta.get('retries', 0)
        if retries < MAX_RETRIES:
            return Request(url=response.url, callback=self.parse, dont_filter=True,
                          meta={'trail': response.meta.get('trail'), 'retries': retries + 1})


class PrimarkCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = PrimarkParseSpider()

    def parse_start_url(self, response):
        trail_part = self.add_trail(response)

        json_data = json.loads(response.body)
        for product in json_data['Products']:
            product_url = 'http://www.primark.com/en/product/' + product['UrlTitle'] + ',' + product['BusinessId']
            yield Request(url=product_url, callback=self.parse_item,  meta={'trail': trail_part})

        if json_data['Products']:
            url = response.url.split('/')
            next_page_r = re.compile('/(\d)/500')
            next_page_url = re.sub(next_page_r, '/' + str(int(re.findall(next_page_r, url)[0]) + 1) + '/500', url)
            yield Request(url=next_page_url, callback=self.parse_start_url, meta={'trail': trail_part})

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        trail_part = response.meta.get('trail', []) + trail_part
        return trail_part

