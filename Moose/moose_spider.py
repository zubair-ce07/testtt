import json
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, clean


class MixinUS:
    retailer = 'moose-us'
    market = 'US'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['http://www.mooseknucklescanada.com/us/']


class MixinUK:
    retailer = 'moose-uk'
    market = 'UK'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['http://www.mooseknucklescanada.com/uk/']


class MixinCA:
    retailer = 'moose-ca'
    market = 'CA'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['http://www.mooseknucklescanada.com']


class MixinEU:
    retailer = 'moose-eu'
    market = 'EU'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['http://www.mooseknucklescanada.com/eu/']


class MooseParseSpider(BaseParseSpider):

    price_css = '.price-box'

    def parse(self, response):

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id[0])
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        availability = clean(response.css('p.availability>span::text'))[0]
        if availability != 'In stock':
            garment['out_of_stock'] = True
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['gender'] = self.detect_gender(self.product_gender(response))

        return garment

    # empty function because product page has no product care fields and the function is required by boilerplate_normal
    def product_care(self, response):
        return []

    def product_id(self, response):
        prod_id = clean(response.css('meta[itemprop=sku]::attr(content)'))
        if not prod_id:
            return clean(response.css('input[name=product]::attr(value)'))
        return prod_id

    def product_name(self, response):
        prod_name = clean(response.css('meta[itemprop=name]::attr(content)'))
        if not prod_name:
            return clean(response.css('.product-name h1::text'))[0]
        return prod_name[0]

    def product_description(self, response):
        first_tab = clean(response.css('div.std ul li ::text'))
        second_tab = clean(response.css('div.std p::text'))[1:]
        return first_tab+second_tab

    def image_urls(self, response):
        return clean(response.css('div.cust-view a::attr(href)'))

    def skus(self, response):
        script_json = self.magento_product_data(response)
        script_json = self.magento_product_map(script_json)
        price = self.product_pricing_common_new(response)
        skus = {}

        for keys, value in script_json.items():
            color = value[0]['label']
            size = value[1]['label']
            skus[keys] = {"color": color, "size": size, "price": price['price'], "currency": price['currency']}

        return skus

    def product_gender(self, response):
        return clean(response.css('tbody>tr>td::text'))[0]


class MooseCrawlSpider(BaseCrawlSpider):

    category_css = "ul.level0>li"
    page_css = ".pages"
    product_css = ".product-image"

    rules = (Rule(LinkExtractor(restrict_css=[category_css, page_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))


class MooseUSParseSpider(MooseParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class MooseUSCrawlSpider(MooseCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = MooseUSParseSpider()


class MooseUKParseSpider(MooseParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class MooseUKCrawlSpider(MooseCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = MooseUKParseSpider()


class MooseCANParseSpider(MooseParseSpider, MixinCA):
    name = MixinCA.retailer + '-parse'


class MooseCANCrawlSpider(MooseCrawlSpider, MixinCA):
    name = MixinCA.retailer + '-crawl'
    parse_spider = MooseCANParseSpider()


class MooseEUParseSpider(MooseParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class MooseEUCrawlSpider(MooseCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = MooseEUParseSpider()
