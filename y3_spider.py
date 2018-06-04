import scrapy
import re
import json

from scrapy.http import Response
from scrapy.spiders import Rule, Request
from w3lib.url import add_or_replace_parameter, url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'y3'
    allowed_domains = ['store.y-3.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'us'
    language = 'ENG'
    currency = 'POUND'
    start_urls = ['http://store.y-3.com/us']
    

class y3ParseSpider(BaseParseSpider):

    def parse(self, response):
        sku_id = self.sku_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus_extractor(response)

        yield garment

    def sku_id(self, response):
        sku_id = re.findall("var jsinit_doubleclick_config=(.+?);", response.text, re.S)[0]
        sku_id = json.loads(sku_id.replace("'", '"'))
        return sku_id['sku']

    def product_gender(self, response):
        gender = re.findall("jsinit_commander=(.+?);", response.text, re.S)[0]
        gender = json.loads(gender)
        return self.detect_gender(gender['GENDER'])

    def skus_extractor(self, response):
        skus = {}
        sizes = self.sizes(response)
        color = self.color(response)

        if sizes:
            for size in sizes:
                skus[color.lower() + '-' + size.lower() if color else size] = self.skus(response, color, size)
        else:
            skus[color.lower()] = self.skus(response, color)

        return skus

    def skus(self, response, color=None, size=None):
        stock_status = self.stock_status(response)
        price = self.price(response)
        previous_price = self.previous_prices(response)

        return {'color': color,
                'size': size,
                'out_of_stock': stock_status,
                'price': price,
                'previous_prices': previous_price}

    def stock_status(self, response):
        stock_status = re.findall("var jsinit_item=(.+?);", response.text, re.S)[0]
        stock_status = json.loads(stock_status)
        return not stock_status['CURRENTITEM']['isAvailable']

    def color(self, response):
        return response.css('.miniThumbsColor>span::text').extract_first()

    def product_name(self, response):
        return response.css('h1::text').extract_first()

    def product_category(self, response):
        return response.css('.microName::text').extract()

    def image_urls(self, response):
        return response.css('#alternateList>div>img::attr(src)').extract()

    def sizes(self, response):
        return response.css('.sizeBoxIn::attr(data-sizewid)').extract() 

    def raw_description(self, response):
        return response.css('.techDescription>li::text').extract()

    def product_care(self, response):
        return [pc for pc in self.raw_description(response) if self.care_criteria(pc)]

    def product_description(self, response):
        return [pd for pd in self.raw_description(response) if not self.care_criteria(pd)]

    def price(self, response):
        return response.css('.newprice>.priceValue::text').extract_first()

    def previous_prices(self, response):
        return response.css('.oldprice>.priceValue::text').extract_first()


class y3CrawlSpider(BaseCrawlSpider):
    allowed_url = r'.*/us/.*'
    listing = '.colonna'
    product = ['.productInfo', '.slick-track']
    
    rules = (Rule(LinkExtractor(allow=allowed_url, restrict_css=listing), callback='parse'),      
             Rule(LinkExtractor(allow=allowed_url, restrict_css=product), callback='parse_item'))


class y3USParseSpider(y3ParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class y3USCrawlSpider(y3CrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = y3USParseSpider()

