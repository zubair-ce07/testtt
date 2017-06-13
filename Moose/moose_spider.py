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


class MixinCan:
    retailer = 'moose-can'
    market = 'CAN'
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

        # adding description from next tab
        garment['description'].append(self.product_description_next_tab(response))
        garment['image_urls'] = self.product_image_urls(response)
        garment['skus'] = self.product_sku(response, sku_id)
        garment['gender'] = self.product_gender(response)

        return garment

    # empty function because product page has no product care fields and the function is required by boilerplate_normal
    def product_care(self, response):
        return None

    def product_id(self, response):
        return clean(response.css('meta[itemprop=sku]::attr(content)').extract_first())

    def product_name(self, response):
        return clean(response.css('meta[itemprop=name]::attr(content)').extract_first())

    def product_description(self, response):
        return clean(response.css('div.std').css('ul>li::text').extract()[1:])

    def product_image_urls(self, response):
        return clean(response.css('div.cust-view').css('a::attr(href)').extract())

    def product_description_next_tab(self, response):
        return clean(response.css('div.std>p::text').extract()[1:])

    def product_price(self, response):
        return clean(response.css('meta[itemprop=price]::attr(content)').extract_first())

    def product_currency(self, response):
        return clean(response.css('meta[itemprop=priceCurrency]::attr(content)').extract_first())

    def product_color_and_size(self, response):
        size_and_color = []
        data = clean(response.css('div[id=product-options-wrapper]>script').extract_first())
        data = data.split('"label":"')
        for i in data:
            i = i.split('","')
            size_and_color.append(i[0])

        break_point = size_and_color.index('Size')
        return clean(size_and_color[2:break_point]), clean(size_and_color[break_point+1:])

    def product_sku(self, response, sku):
        colors, sizes = self.product_color_and_size(response)
        price = self.product_pricing_new(response)
        availability = self.product_availability(response)
        skus = {}

        for color in colors:
            for size in sizes:
                skus[sku+"_"+size+"_"+color] = {"color": color, "size": size, "price": price,
                                                "availability": availability}

        return skus

    def product_availability(self, response):
        return clean(response.css('p.availability>span::text').extract_first())

    def product_gender(self, response):
        return clean(response.css('tbody>tr>td::text').extract_first())


class MooseCrawlSpider(BaseCrawlSpider):

    category_css = "ul.level0>li"
    page_css = "div.pages"
    product_css = "a.product-image"

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


class MooseCANParseSpider(MooseParseSpider, MixinCan):
    name = MixinCan.retailer + '-parse'


class MooseCANCrawlSpider(MooseCrawlSpider, MixinCan):
    name = MixinCan.retailer + '-crawl'
    parse_spider = MooseCANParseSpider()


class MooseEUParseSpider(MooseParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class MooseEUCrawlSpider(MooseCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = MooseEUParseSpider()
