import re
import json

from scrapy.http import Response
from scrapy.spiders import Rule, Request

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean

class Mixin:
    retailer = 'y3'
    allowed_domains = ['store.y-3.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    currency = 'GBP'
    start_urls = ['http://store.y-3.com/us/y3store/sleeveless-t-shirt_cod12177083tm.html']
    

class Y3ParseSpider(BaseParseSpider):
    price_css = '#productInfo .price .prices'

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
        sizes = ''
        raw_skus = self.raw_skus(response)
        colour = self.colour(raw_skus)
        common_sku = self.product_pricing_common(response)

        if not raw_skus['CURRENTITEM']['json']:
            skus[colour.lower()] = common_sku
            return skus

        sizes = self.sizes(raw_skus)
        common_sku['colour'] = colour

        if self.out_of_stock(raw_skus):
            common_sku['out_of_stock'] = True

        available_sizes = self.available_sizes(raw_skus)

        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size

            if size not in available_sizes:
                sku['out_of_stock'] = True
            
            skus[colour.lower() + '-' + size.lower() if colour else size] = sku 

        return skus

    def out_of_stock(self, raw_skus):
        return not raw_skus['CURRENTITEM']['isAvailable']

    def colour_id(self, raw_skus):
        return raw_skus['CURRENTITEM']['json']['Quantity'][0]['ColorId']

    def colour(self, raw_skus):
        color_id = self.colour_id(raw_skus)
        return raw_skus['COLORS'][color_id]['desc']

    def product_name(self, response):
        return clean(response.css('h1::text'))

    def product_category(self, response):
        return clean(response.css('.microName::text'))

    def image_urls(self, response):
        return clean(response.css('#alternateList>div>img::attr(src)'))

    def raw_skus(self, response):
        raw_skus = re.findall('var jsinit_item=(.+?);', response.text, re.S)[0]
        return json.loads(raw_skus)

    def sizes(self, raw_skus):
        return raw_skus['CURRENTITEM']['json']['Colors'][0]['SizeW']

    def available_sizes(self, raw_skus):
        sizes = raw_skus['CURRENTITEM']['json']['SizeW']
        return [size['DefaultSize'] for size in sizes]

    def out_of_stock_sizes(self, response):
        return clean(response.css('#itemSizes>.disbaled::text'))

    def raw_description(self, response):
        return clean(response.css('.techDescription>li::text'))

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
