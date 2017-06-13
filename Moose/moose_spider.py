import json
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
        garment['skus'] = self.skus(response, sku_id)
        garment['gender'] = self.detect_gender(self.product_gender(response))

        availability = clean(self.product_availability(response))
        if availability != 'In stock':
            garment['out_of_stock'] = True

        return garment

    # empty function because product page has no product care fields and the function is required by boilerplate_normal
    def product_care(self, response):
        return []

    def product_id(self, response):
        return clean(response.css('meta[itemprop=sku]::attr(content)').extract_first())

    def product_name(self, response):
        return clean(response.css('meta[itemprop=name]::attr(content)').extract_first())

    def product_description(self, response):
        first_tab = clean(response.css('div.std').css('ul>li::text').extract()[1:])
        second_tab = clean(response.css('div.std>p::text').extract()[1:])
        return first_tab+second_tab

    def image_urls(self, response):
        return clean(response.css('div.cust-view a::attr(href)').extract())

    def product_color_and_size(self, response):
        colors = []
        sizes = []
        script_json = clean(response.css('div[id=product-options-wrapper]>script::text').extract_first())
        script_json = script_json[script_json.find('{'):]
        script_json = script_json[:-2]
        parsed_json_data = json.loads(script_json)
        color_dict = parsed_json_data['attributes']['141']['options']
        size_dict = parsed_json_data['attributes']['142']['options']
        for col in color_dict:
            colors.append(col['label'])
        for siz in size_dict:
            sizes.append(siz['label'])
        return colors, sizes

    def skus(self, response, sku):
        colors, sizes = self.product_color_and_size(response)
        price = self.product_pricing_new(response)
        skus = {}

        for color in colors:
            for size in sizes:
                skus[color+"_"+size] = {"color": color, "size": size, "price": price}

        return skus

    def product_availability(self, response):
        return clean(response.css('p.availability>span::text').extract_first())

    def product_gender(self, response):
        return clean(response.css('tbody>tr>td::text').extract_first())


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
