from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider


class Mixin:
    retailer = 'Moose-us'
    market = 'US'
    lang = 'Eng'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['http://www.mooseknucklescanada.com/us/']


class MooseParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'
    price_css = 'div[itemprop=offers]'

    def parse(self, response):

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['brand'] = 'Moose'
        garment['name'] = self.product_name(response)
        garment['description'], garment['care'] = \
            self.extract_care_from_description(response, self.product_details(response))

        garment['url'] = response.url
        garment['image_urls'] = self.product_image_urls(response)
        garment['skus'] = self.product_sku(response, sku_id)
        garment['gender'] = self.product_gender(response)

        return garment

    # empty function because product page has no product care fields and the function is required by boilerplate_normal
    def product_care(self, response):
        return None

    def extract_care_from_description(self,response, description):
        care = []
        for line in description:
            if self.care_criteria_simplified(line):
                care.append(line)
        description = [x for x in description if x not in care]
        description.append(self.product_description(response))
        return description, care


    def product_id(self, response):
        return self.sanitize(response.css('meta[itemprop=sku]::attr(content)').extract_first())

    def product_name(self, response):
        return self.sanitize(response.css('meta[itemprop=name]::attr(content)').extract_first())

    def product_details(self, response):
        return self.sanitize(response.css('div.std').css('ul>li::text').extract()[1:])

    def product_image_urls(self, response):
        return self.sanitize(response.css('div.cust-view').css('a::attr(href)').extract())

    def product_description(self, response):
        return self.sanitize(response.css('div.std>p::text').extract()[1:])

    def product_price(self, response):
        return self.sanitize(response.css('meta[itemprop=price]::attr(content)').extract_first())

    def product_currency(self, response):
        return self.sanitize(response.css('meta[itemprop=priceCurrency]::attr(content)').extract_first())

    def product_color_and_size(self, response):
        size_and_color = []
        data = self.sanitize(response.css('div[id=product-options-wrapper]>script').extract_first())
        data = data.split('"label":"')
        for i in data:
            i = i.split('","')
            size_and_color.append(i[0])

        break_point = size_and_color.index('Size')
        return self.sanitize(size_and_color[2:break_point]), self.sanitize(size_and_color[break_point+1:])

    def product_sku(self, response, sku):
        colors, sizes = self.product_color_and_size(response)
        price = self.product_pricing_new(response)
        availability = self.product_availability(response)
        skus={}

        for color in colors:
            for size in sizes:
                skus[sku+"_"+size+"_"+color] = {"color": color, "size": size, "price": price,
                                                "availability": availability}

        return skus

    def product_availability(self, response):
        return self.sanitize(response.css('p.availability>span::text').extract_first())

    def product_gender(self, response):
        return self.sanitize(response.css('tbody>tr>td::text').extract_first())


class MooseCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseParseSpider()

    category_css = "ul.level0>li"
    page_css = "div.pages"
    product_css = "a.product-image"

    rules = (Rule(LinkExtractor(restrict_css=category_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=page_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))