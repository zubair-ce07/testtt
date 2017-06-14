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

    price_css = 'div[itemprop=offers]'

    def parse(self, response):

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['gender'] = self.detect_gender(self.product_gender(response))

        return garment

    # empty function because product page has no product care fields and the function is required by boilerplate_normal
    def product_care(self, response):
        return []

    def product_id(self, response):
        return clean(response.css('meta[itemprop=sku]::attr(content)'))[0]

    def product_name(self, response):
        return clean(response.css('meta[itemprop=name]::attr(content)'))[0]

    def product_description(self, response):
        first_tab = clean(response.css('div.std ul>li::text'))[1:]
        second_tab = clean(response.css('div.std>p::text'))[1:]
        return first_tab+second_tab

    def image_urls(self, response):
        return clean(response.css('div.cust-view a::attr(href)'))

    def product_color_and_size(self, response):
        colors = []
        sizes = []
        color_codes = []
        size_codes = []

        script_json = self.magento_product_data(response)
        colors_dict = script_json['attributes']['141']['options']
        if '142' in script_json.get('attributes', {}):
            sizes_dict = script_json['attributes']['142']['options']
        else:
            sizes_dict = script_json['attributes']['143']['options']
        for color in colors_dict:
            colors.append(color['label'])
            color_codes.append(color['products'])
        for size in sizes_dict:
            sizes.append(size['label'])
            size_codes.append(size['products'])
        return self.create_sku_keys(colors, sizes, color_codes, size_codes)

    def create_sku_keys(self, colors, sizes, color_codes, size_codes):
        sku_keys = []
        itera = 0
        for color in colors:
            next = 0
            for size in sizes:
                if not set(color_codes[itera]).isdisjoint(size_codes[next]):
                    sku_keys.append(color+"_"+size)
                next += 1
        return sku_keys

    def skus(self, response):
        sku_keys = self.product_color_and_size(response)
        price = self.product_pricing_new(response)
        skus = {}
        availability = self.product_availability(response)

        for keys in sku_keys:
            color_size = keys.split('_')
            skus[keys] = {"color": color_size[0], "size": color_size[1], "price": price[1], "currency": price[2],
                          "out_of_stock": availability}

        return skus

    def product_availability(self, response):
        availability = clean(response.css('p.availability>span::text'))[0]
        flag = False
        if availability != 'In stock':
            flag = True
        return flag

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
