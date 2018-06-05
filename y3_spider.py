import scrapy
import re
import json

from ast import literal_eval
from scrapy.http import Response
from scrapy.spiders import Rule, Request
from w3lib.url import add_or_replace_parameter, url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean
from skuscraper.parsers.jsparser import JSParser


class Mixin:
    retailer = 'y3'
    allowed_domains = ['store.y-3.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    currency = 'GBP'
    start_urls = ['http://store.y-3.com/us']
    

class Y3ParseSpider(BaseParseSpider):
    price_css = '.prices'

    def parse(self, response):
        sku_id = self.sku_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        yield garment

    def sku_id(self, response):
        sku_id = clean(response.xpath('//script//text()').re("'sku'\s:\s(.*)"))
        return sku_id[0]

    def product_gender(self, response):
        gender = clean(response.xpath('//script//text()').re('"GENDER":\s"(\w+)"'))
        return self.gender_lookup(gender[1])

    def skus(self, response):
        skus = {}
        sizes = self.sizes(response)
        color = self.color(response)

        previous_price, price, currency = self.product_pricing(response)

        common_sku = {'color': color,
                      'out_of_stock': self.out_of_stock(response),
                      'price': price,
                      'previous_price': previous_price[0],
                      'currency': currency}

        if sizes:
            for size in sizes:
                if self.out_of_stock(response):
                    common_sku['out_of_stock'] = True
                common_sku['size'] = size
                skus[color.lower() + '-' + size.lower() if color else size] = common_sku 
        else:
            skus[color.lower()] = common_sku

        return skus

    def out_of_stock(self, response):
        out_of_stock = clean(response.xpath('//script//text()').re('"isAvailable":\s(\w+)'))
        return not out_of_stock[0]

    def color(self, response):
        return clean(response.css('.miniThumbsColor>span::text').extract_first())

    def product_name(self, response):
        return clean(response.css('h1::text').extract_first())

    def product_category(self, response):
        return clean(response.css('.microName::text').extract())

    def image_urls(self, response):
        return clean(response.css('#alternateList>div>img::attr(src)').extract())

    def sizes(self, response):
        return clean(response.css('.sizeBoxIn::attr(data-sizewid)').extract()) 

    def raw_description(self, response):
        return clean(response.css('.techDescription>li::text').extract())

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]


class Y3CrawlSpider(BaseCrawlSpider):
    listing = '.colonna'
    product = ['.productInfo', '.slick-track']
    
    rules = (Rule(LinkExtractor(restrict_css=listing), callback='parse'),      
             Rule(LinkExtractor(restrict_css=product), callback='parse_item'))


class Y3USParseSpider(Y3ParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class Y3USCrawlSpider(Y3CrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = Y3USParseSpider()
