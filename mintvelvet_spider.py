# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean, tokenize
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.http import Request
from urlparse import urlparse
import re


class Mixin(object):
    retailer = 'mintvelvet-uk'
    allowed_domains = ['www.mintvelvet.co.uk', 'fashion.mintvelvet.co.uk']
    market = 'UK'
    start_urls = ['http://www.mintvelvet.co.uk']


class MintVelvetParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//p[@class='product_price']//text()"
    take_first = TakeFirst()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        pid = self.product_id(response.url)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, hxs, response)

        if 'candles' in response.url:
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = 'women'

        garment['merch_info'] = self.merch_info(hxs, response.url)
        garment['skus'] = self.skus(hxs)
        image_requests, garment['image_urls'] = self.image_urls(hxs)
        garment['meta'] = {'requests_queue': image_requests}

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']

        if response.status != 404 and response.url not in garment['image_urls']:
            garment['image_urls'] += [response.url]
            img_url = response.url.split('.jpg')[0].split('_')
            next_img_url = img_url[0] + '_' + str(int(img_url[1]) + 1) + '.jpg'
            garment['meta']['requests_queue'] += [Request(url=next_img_url, callback=self.parse_images,
                                                          dont_filter=True, meta={'handle_httpstatus_list': [404]})]
        if not garment['meta']['requests_queue']:
            if len(garment['image_urls']) > 3:
                garment['image_urls'].insert(0, garment['image_urls'].pop(2))

        return self.next_request_or_garment(garment)

    def skus(self, hxs):
        skus = {}
        oos_xpath_t = "//span[text()='%s']/ancestor::li/@class"
        sku_id1_xpath_t = "//span[text()='%s']/ancestor::li/@data-value"
        sku_id2_xpath_t = "//span[text()='%s']/preceding-sibling::input/@value"
        previous_price, price, currency = self.product_pricing(hxs)

        color = " ".join(clean(self.detect_colour(x) for x in tokenize(self.product_name(hxs))))
        sizes = clean(hxs.select("//div[@class='size_selector']//ul//li//span[1]/text()"))

        for size in sizes:
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color,
                'out_of_stock': 'no_stock' in self.take_first(clean(hxs.select(oos_xpath_t % size))),
            }

            if previous_price:
                sku['previous_prices'] = [previous_price]

            sku_id = self.take_first(clean(hxs.select(sku_id1_xpath_t % size)) or
                                     clean(hxs.select(sku_id2_xpath_t % size)))
            skus[sku_id] = sku

        return skus

    def product_id(self, url):
        return urlparse(url).path.split('/')[-1]

    def product_brand(self, hxs):
        return "Mint Velvet"

    def image_urls(self, hxs):
        image_url = self.take_first(clean(hxs.select("//a[@class='zoom']/@href")))
        next_img_url = image_url.split('.jpg')[0] + '_1.jpg'
        return [Request(url=next_img_url, callback=self.parse_images)], [image_url]

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//h1[@itemprop='name']/text()")))

    def product_category(self, hxs):
        return list(set(clean(hxs.select("//div[@id='breadcrumbs']//text()"))[1:-1]))

    def product_description(self, hxs):
        return clean(hxs.select("//div[@class='product_description']//text()"))

    def product_care(self, hxs):
        return clean(hxs.select("//dd[@id='product_details']/p/text()"))

    def merch_info(self, hxs, url):
        des_cat_and_url = ' '.join(self.product_description(hxs) + self.product_category(hxs) + [url])
        if re.findall('web.exclusive', des_cat_and_url, re.I):
            return ["Web Exclusive"]


class MintVelvetCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MintVelvetParseSpider()
    listings_x = [
        "//a[contains(@class,'pageselectornext')]",
        "//ul[@class='dropdown dl-menu']//li/a",
    ]

    products_x = [
        "//div[@id='sli_results_container']//li/a[1]",
        "//ul[@class='row category-product-list product-list-medium']//a[1]",
    ]

    deny_r = ['magazine', 'wish-list', 'winter15-catalogue', 'dropdownchristmas']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x, deny=deny_r), callback='parse'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    )
