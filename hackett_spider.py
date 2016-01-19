# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider, tokenize, CurrencyParser
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from base import clean
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
import json
from scrapy.http import Request
import re


class Mixin(object):
    market = 'UK'
    retailer = 'hackett-uk'
    allowed_domains = ['www.hackett.com']
    start_urls = ['http://www.hackett.com/gb/']


class HackettParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'
    take_first = TakeFirst()
    price_x = "//div[@class='product-shop']//span[contains(@id,'price')]//text()"
    skus_x = "//script[contains(text(), 'new Product.Config(')]//text()"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(hxs)
        if not hxs.select(self.skus_x):
            return self.out_of_stock_garment(response, pid)

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        garment['gender'] = self.product_gender(hxs)
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'], color_ids = self.skus(hxs)
        garment['meta'] = {'requests_queue': self.image_requests(response, color_ids)}

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        hxs = HtmlXPathSelector(response)

        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(hxs)

        return self.next_request_or_garment(garment)

    def skus(self, hxs):
        skus, color_ids = {}, []

        skus_info = self.take_first(clean(hxs.select(self.skus_x)))
        skus_info = json.loads(re.findall('Product.Config\(({.*})\); lwParams', skus_info)[0])

        colors = skus_info.get('attributes').get('85', {}).get('options', [])
        sizes = skus_info.get('attributes').get('171', {}).get('options', [])
        lengths = skus_info.get('attributes').get('172', {}).get('options', [])

        previous_price, base_price, currency = self.product_pricing(hxs)

        skus, color_ids = self.set_colors(colors, skus)
        skus = self.set_sizes(sizes, lengths, skus)
        skus = self.set_lengths(lengths, skus)

        for sku_id in skus:
            sku = {
                'price': skus[sku_id].get('price', 0) + base_price,
                'currency': currency,
            }

            if sku['price'] == skus[sku_id]['previous_prices'][0]:
                skus[sku_id].pop('previous_prices')

            skus[sku_id].update(sku)

        return skus, color_ids

    def set_colors(self, colors, skus):
        color_ids = []
        for color in colors:
            color_ids += [color['id']]
            for product in color['products']:
                skus[product] = {
                    'colour': color['label'],
                }
        return skus, color_ids

    def set_sizes(self, sizes, lengths, skus):
        for size in sizes:
            for product in size['products']:
                sku = {
                    'size': self.one_size if size['label'] in ['000', 'ONE SIZE'] else size['label'],
                }

                if not lengths:
                    sku_price = {
                        'price': CurrencyParser.float_conversion(float(size['price'])),
                        'previous_prices': [CurrencyParser.float_conversion(float(size['oldPrice']))],
                    }
                    sku.update(sku_price)

                if product in skus:
                    skus[product].update(sku)
                else:
                    skus[product] = sku
        return skus

    def set_lengths(self, lengths, skus):
        for length in lengths:
            for product in length['products']:
                sku = {
                    'size': skus[product]['size'] + '/' + length['label'],
                    'price': CurrencyParser.float_conversion(float(length['price'])),
                    'previous_prices': [CurrencyParser.float_conversion(float(length['oldPrice']))],
                }
                skus[product].update(sku)
        return skus

    def image_requests(self, response, color_ids):
        hxs = HtmlXPathSelector(response)
        requests = []

        url_t = 'http://www.hackett.com/gb/optiongallery/index/index/?isAjax=1&variation=%s&product=%s'
        product_id = self.product_id(hxs)

        for color_id in color_ids:
            if color_id not in response.url:
                url = url_t % ('{"85":' + color_id + '}', product_id)
                requests += [Request(url, callback=self.parse_images)]
        return requests

    def product_gender(self, hxs):
        if "kids" in tokenize(self.product_category(hxs)):
            return "boys"
        return "men"

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("//input[@name='product']/@value")))

    def product_brand(self, hxs):
        cat_name = ' '.join(self.product_category(hxs) + [self.product_name(hxs)]).lower()

        if 'aston martin' in cat_name:
            return "Aston Martin"

        if 'murdock' in cat_name:
            return "Murdock"

        return "Hackett"

    def image_urls(self, hxs):
        xpath = "//ul[contains(@class,'thumbnails')]//li//a[@class='full-size']/@href"
        return clean(hxs.select(xpath))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//li[@class='product']//text()")))

    def product_category(self, hxs):
        return clean(hxs.select("//div[@class='breadcrumbs']//li/a/text()"))[1:]

    def raw_description(self, hxs):
        return clean(hxs.select("//div[@class='tabs-content']//text()"))

    def product_description(self, hxs):
        return [rd for rd in self.raw_description(hxs) if not self.care_criteria(rd)]

    def product_care(self, hxs):
        care = self.take_first(clean(hxs.select("//div[@class='product-attributtes']//text()")))
        care = care.split('~')[0]
        return [care] + [rd for rd in self.raw_description(hxs) if self.care_criteria(rd)]


class HackettCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = HackettParseSpider()

    listings_x = [
        "//li[contains(@class,'level')]//a[not(following-sibling::ul)]",
        "//li[@class='current']/following-sibling::li[1]//a",
    ]
    products_x = [
        "//div[@class='faux-column']//li/a",
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x),
             callback='parse'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x)
             , callback='parse_item')
    )
