# -*- coding: utf-8 -*-
from base import BaseParseSpider, BaseCrawlSpider
from base import clean
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse


class Mixin(object):
    retailer = 'blackrainbow-shop-fr'
    allowed_domains = ['www.blackrainbow-shop.com']
    market = 'FR'
    lang = 'fr'
    start_urls = ['http://www.blackrainbow-shop.com/fr/']


class BlackrainbowShopParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    price_x = "//span[@id='old_price_display']/text() | //span[@id='our_price_display']/text()"
    take_first = TakeFirst()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        pid = self.product_id(hxs)
        garment = self.new_unique_garment(pid)
        if garment is None:
            return
        if self.out_of_stock(hxs):
            return self.out_of_stock_garment(response, pid)
        self.boilerplate_normal(garment, hxs, response)
        garment['category'] = self.product_category(response.url)
        garment['image_urls'] = self.image_urls(hxs)
        garment['skus'] = self.skus(hxs)
        return garment

    def skus(self, hxs):
        skus = {}
        color = self.detect_colour(self.product_name(hxs).lower().replace('/', ' '))
        sizes = clean(hxs.select("//div[@id='attributes']/select/option/text()")) or [self.one_size]
        products_data = [x.split(', ') for x in clean(hxs.select("//div[@id='center_column']/script/text()")
                                                      .re('addCombination\((.*)\);'))]
        previous_price, price, currency = self.product_pricing(hxs)

        for index, size in enumerate(sizes):
            size = self.one_size if size == 'TU' else size
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color,
                'out_of_stock': products_data[index][2] == '0' if products_data else False,
            }
            if previous_price:
                sku['previous_prices'] = [previous_price]
            key = products_data[index][0] if products_data else color + '_' + size
            skus[key] = sku
        return skus

    def out_of_stock(self, hxs):
        return bool(hxs.select
                    ('''//span[@id="availability_value"][contains(text(),"Ce produit n'est plus en stock")]'''))

    def product_id(self, hxs):
        return self.take_first(clean(hxs.select("(//input[@name='id_product']/@value)[1]")))

    def image_urls(self, hxs):
        return clean(hxs.select("//div[@id='thumbs_list']//a/@href"))

    def product_name(self, hxs):
        return self.take_first(clean(hxs.select("//div[@class='title title-black']//text()")))

    def product_category(self, url):
        return urlparse(url).path.split('/')[2:-1] if isinstance(url, str) else None

    def product_brand(self, hxs):
        return self.take_first(clean(hxs.select("//div[@class='brand']//img/@alt"))) \
               or self.product_name(hxs).split()[0]

    def product_description(self, hxs):
        return []

    def product_care(self, hxs):
        return []


class BlackrainbowShopCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BlackrainbowShopParseSpider()
    listings_x = [
        "//a[text()='HAUTS' or text()='BAS' or text()='CHAUSSURES' or text()='ACCESSOIRES']/following::ul[1]/li",
    ]
    products_x = [
        "//ul[@id='list-products']//li/a",
    ]
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=listings_x), callback='parse_and_add_men'),
        Rule(SgmlLinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    )
